#!/bin/bash

# Function to create a PR using Claude Code based on a GitHub issue
# Supports repositories with submodules
create_claude_pr() {
  # Parse arguments
  local repo_owner="napistu"
  local main_repo_name="napistu"
  local submodule_name=""
  local issue_number=""
  local base_branch="main"
  local conventions_path="./conventions.md"
  local reviewer="shackett"
  
  # Parse command line arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --main-repo=*)
        local repo="${1#*=}"
        # Extract owner and name from repo string (format: owner/name)
        repo_owner="${repo%%/*}"
        main_repo_name="${repo##*/}"
        shift
        ;;
      --submodule=*)
        submodule_name="${1#*=}"
        shift
        ;;
      --issue=*)
        issue_number="${1#*=}"
        shift
        ;;
      --base=*)
        base_branch="${1#*=}"
        shift
        ;;
      --conventions=*)
        conventions_path="${1#*=}"
        shift
        ;;
      --reviewer=*)
        reviewer="${1#*=}"
        shift
        ;;
      *)
        echo "Unknown parameter: $1"
        return 1
        ;;
    esac
  done
  
  # Validate required parameters
  if [[ -z "$repo_owner" || -z "$main_repo_name" || -z "$submodule_name" || -z "$issue_number" ]]; then
    echo "Error: Required parameters missing"
    echo "Usage: create_claude_pr --main-repo=owner/name --submodule=submodule_name --issue=123 [--base=main] [--conventions=./conventions.md] [--reviewer=username]"
    return 1
  fi
  
  # Construct paths and repository references
  local submodule_path="lib/${submodule_name}"
  local submodule_repo="${repo_owner}/${submodule_name}"
  
  # Check if conventions file exists
  if [[ ! -f "$conventions_path" ]]; then
    echo "Error: Conventions file not found at $conventions_path"
    return 1
  fi
  
  # Create branch name based on issue number
  local branch_name="fix-issue-${issue_number}"
  
  # Fetch issue details from the submodule repository
  echo "Fetching issue #${issue_number} details from ${submodule_repo}..."
  local issue_title=$(gh issue view "$issue_number" --repo "${submodule_repo}" --json title --jq .title)
  local issue_body=$(gh issue view "$issue_number" --repo "${submodule_repo}" --json body --jq .body)
  
  if [[ -z "$issue_title" ]]; then
    echo "Error: Could not fetch issue details. Check if the issue exists and you have permissions."
    return 1
  fi
  
  # Make sure we're on the latest base branch in the main repository
  echo "Updating main repository base branch..."
  git fetch origin "$base_branch"
  git checkout "$base_branch"
  git pull origin "$base_branch"
  
  # Update submodules
  echo "Updating submodules..."
  git submodule update --init --recursive
  
  # Create and checkout a new branch for the fix in the main repository
  echo "Creating branch in main repository: $branch_name"
  git checkout -b "$branch_name"
  
  # Check if submodule path exists
  if [[ ! -d "$submodule_path" ]]; then
    echo "Error: Submodule path not found: $submodule_path"
    return 1
  fi
  
  # Navigate to submodule
  echo "Navigating to submodule: $submodule_path"
  cd "$submodule_path" || { echo "Failed to navigate to submodule"; return 1; }
  
  # Update submodule and create a branch
  echo "Creating branch in submodule..."
  git checkout "$base_branch"
  git pull origin "$base_branch"
  git checkout -b "$branch_name"
  
  # Copy conventions file to temp location
  local conventions_copy=$(mktemp)
  cp "$OLDPWD/$conventions_path" "$conventions_copy"
  
  # Use Claude Code to analyze the issue and generate changes
  echo "Analyzing issue with Claude Code in submodule: $submodule_name"
  local temp_dir=$(mktemp -d)
  
  # Call Claude Code to analyze the issue
  # Note: This is a simplified version, as exact Claude Code CLI syntax may vary
  claude-code analyze \
    --repo="${submodule_repo}" \
    --issue="$issue_number" \
    --conventions="$conventions_copy" \
    --output-dir="$temp_dir" \
    --prompt="Please analyze issue #${issue_number}: '${issue_title}' and propose code changes that follow our conventions."
  
  # Check if Claude Code was successful
  if [[ $? -ne 0 ]]; then
    echo "Error: Claude Code analysis failed"
    # Clean up
    rm -f "$conventions_copy"
    cd "$OLDPWD"
    return 1
  fi
  
  # Apply the changes to the submodule
  echo "Applying generated changes to submodule..."
  if [[ -d "$temp_dir" && "$(ls -A "$temp_dir")" ]]; then
    cp -r "$temp_dir"/* .
    
    # Check if any files were changed
    if [[ -z "$(git status --porcelain)" ]]; then
      echo "No changes were made by Claude Code"
      rm -f "$conventions_copy"
      cd "$OLDPWD"
      return 0
    fi
    
    # Add all changes in submodule
    git add .
    
    # Commit the changes in submodule
    git commit -m "Fix #${issue_number}: ${issue_title}"
    
    # Push the submodule branch
    echo "Pushing changes in submodule..."
    git push -u origin "$branch_name"
    
    # Navigate back to parent repository
    cd "$OLDPWD" || { echo "Failed to navigate back to parent repository"; return 1; }
    
    # Update the submodule reference in the parent repository
    git add "$submodule_path"
    git commit -m "Update submodule reference for fix #${issue_number}"
    
    # Push the main repository branch
    git push -u origin "$branch_name"
    
    # Create PR in the submodule repository first
    echo "Creating PR in submodule repository..."
    local submodule_pr_body="This PR addresses issue #${issue_number}.\n\n${issue_body}\n\nChanges were proposed by Claude Code based on our conventions."
    
    # Add reviewer if provided
    local reviewer_flag=""
    if [[ -n "$reviewer" ]]; then
      reviewer_flag="--reviewer $reviewer"
      submodule_pr_body+="\n\ncc @${reviewer}"
    fi
    
    # Create PR in the submodule repo
    local submodule_pr_url=$(gh pr create \
      --repo="${submodule_repo}" \
      --title "Fix #${issue_number}: ${issue_title}" \
      --body "$submodule_pr_body" \
      --base "$base_branch" \
      $reviewer_flag \
      --json url --jq .url)
    
    # Create PR in the main repository
    echo "Creating PR in main repository..."
    local main_pr_body="This PR updates the submodule reference for issue #${issue_number}.\n\nSubmodule PR: ${submodule_pr_url}\n\nThis PR points to the updated submodule which contains the actual code changes."
    
    if [[ -n "$reviewer" ]]; then
      main_pr_body+="\n\ncc @${reviewer}"
    fi
    
    gh pr create \
      --repo="${repo_owner}/${main_repo_name}" \
      --title "Update submodule for issue #${issue_number}: ${issue_title}" \
      --body "$main_pr_body" \
      --base "$base_branch" \
      $reviewer_flag
    
    echo "PRs created successfully! 🎉"
    echo "Submodule PR: ${submodule_pr_url}"
  else
    echo "No changes were generated by Claude Code"
  fi
  
  # Clean up
  rm -rf "$temp_dir"
  rm -f "$conventions_copy"
}

# Check if being sourced or executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  # Script is being executed directly, call the function with all arguments
  create_claude_pr "$@"
fi