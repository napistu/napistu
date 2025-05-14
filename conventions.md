# Code Conventions

## General Guidelines
- Maximum line length: 100 characters
- Indentation: 2 spaces (no tabs)
- File encoding: UTF-8
- Line endings: LF (Unix-style)
- Files should end with a single newline

## Naming Conventions
- Variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Classes/Interfaces: PascalCase
- Private members: _prefixed_snake_case
- Temporary variables: Avoid single-letter names except in loops
- Boolean variables: Should start with "is_", "has_", "should_", etc.

## Code Organization
- One class per file
- Related functions grouped together
- Import statements ordered: standard library, third-party, local
- Maximum function length: 30 lines
- Maximum file length: 500 lines

## Documentation
- Public API methods require docstring comments
- Complex algorithms need explanatory comments
- TODO/FIXME comments format: `# TODO(username): description`
- Include examples for non-obvious usage

## Testing Requirements
- Test file naming: `test_{original_filename}.py` or `{original_filename}_test.R`
- Every public function requires at least one positive and one negative test
- Mock external dependencies
- Test coverage requirement: minimum 85%
- Use descriptive test names following "test_should_do_something_when_condition" pattern

## Language-Specific Guidelines

### Python
- Follow Black code formatting style
- Code must pass Ruff linter checks
- Use type hints
- Prefer list/dict comprehensions for simple transformations
- Place utility functions as the bottom of each file and add an underscore prefix
- Use context managers for resource management
- Place constants in a package- or module-level constants.py files
- Maximum function arguments: 5

### R (Tidyverse Style)
- Use snake_case for all names (variables, functions)
- Place spaces around all infix operators (`=`, `+`, `-`, `<-`, etc.)
- Use `<-` rather than `=` for assignment
- Limit code to 80 characters per line
- Indent with two spaces (never tabs)
- Function calls: no space before parentheses, e.g., `mean(x)`
- Commas: always followed by a space, no space before
- Assignment: spaces around `<-`
- Code blocks: {curly braces} on same line as function declaration, new line before closing brace
- Use the pipe operator `%>%` for data transformations
- Use `purrr` functions instead of `apply` family
- Use `tibble` instead of `data.frame`
- Function documentation using roxygen2 format
- Avoid `attach()`, `setwd()`, `library()` in scripts (use `box::use()` or similar)
- End each script file with `# End of script`

## Git Practices
- Commit messages: follow conventional commits format
- PR descriptions: include issue reference, summary of changes, testing notes
- Branch naming: `issue-` prefix followed by issue number. If this branch already exists then create a new branch with a -2, -3, ... suffix 

## Project-Specific Patterns

### State management

- Single source of truth for application state
- Immutable state updates
- Predictable state transitions
- Functions should not have both main effects and side effects
- Clear separation between state and UI logic
- Log state changes at appropriate levels (debug/info)

###  Configuration Management

#### Security
- Never commit sensitive values (API keys, tokens, passwords)
- Use environment variables for sensitive configuration in production
- Document all sensitive configuration parameters
- Implement secure loading of credentials

#### Validation
- Validate configurations at startup
- Provide clear error messages for missing or invalid configurations
- Include type validation and constraints (min/max values, etc.)
- Document all available configuration options with:
  - Parameter name
  - Type and constraints
  - Default value
  - Description
  - Example
- Use Pydantic and typehints to validate Python configuration objects and files
- Use checkthat to validate R arguments

### Logging
- use logger for Python reporting
- use cli for R reporting
