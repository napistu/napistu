# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Napistu is a project for creating and working with genome-scale mechanistic networks. It allows pathways of interest to be created from multiple sources (e.g., Reactome, STRING, TRRUST), aggregated across sources, and refined with additional information. This pathway representation can be turned into a graphical network to identify molecular neighborhoods, find paths between molecules, and perform network propagation.

The repository consists of three main components:
- **napistu-py**: Python library with core implementations of pathway representations and network-based searches
- **napistu-r**: R library for network visualization and utilities called from napistu-py
- **napistu-scrapyard**: Collection of applications and experimental code

## Development Environment Setup

### Python Library

```bash
# Create and activate virtual environment
uv venv --python 3.11
source .venv/bin/activate

# Install the Python package with development dependencies
cd lib/napistu-py
uv pip install -e ".[dev]"

# To include rpy2 support
uv pip install -e ".[dev,rpy2]"
```

### R Package

```bash
# Install from local source in R
R CMD build lib/napistu-r
R CMD INSTALL rcpr_*.tar.gz

# Or install in an interactive R session
R
> remotes::install_local("lib/napistu-r")
```

### Tutorials Environment

```bash
# Create and activate virtual environment
uv venv --python 3.11
source .venv/bin/activate

# Install dependencies
uv pip install --upgrade pip wheel setuptools ipykernel jupyter
uv pip install './lib/napistu-py[rpy2]'
uv pip install pycairo seaborn

# Set up Jupyter kernel
python -m ipykernel install --name napistu_tutorials --display-name "Napistu - Tutorials" --user
```

## Common Commands

### Python Library Commands

```bash
# Activate the virtual environment (from repository root directory)
source tutorials/.venv/bin/activate

# Change to the Python package directory
cd lib/napistu-py

# Run tests
python -m pytest                        # Run all tests
python -m pytest -xvs src/tests/test_utils.py  # Run a specific test file
python -m pytest -xvs src/tests/test_utils.py::test_function_name  # Run a specific test

# Run with coverage report
python -m pytest --cov=napistu

# Run linting
ruff check .              # Lint the codebase
ruff format .             # Format code

# Build the package
uv pip install build
python -m build
```

### R Package Commands

```bash
# Change to the R package directory
cd lib/napistu-r

# Run tests
R -e "devtools::test()"          # Run all tests
R -e "devtools::test_file('tests/testthat/test-netcontextr_context.R')"  # Run a specific test file

# Check the package
R CMD check .
R -e "devtools::check()"

# Build documentation
R -e "devtools::document()"
```

## Code Structure

### Python Library (`lib/napistu-py/src/napistu/`)

- **consensus.py**: Functions for merging complementary data sources
- **constants.py**: Package-level constants
- **gcs/**: Google Cloud Storage functionality
- **ingestion/**: Modules for importing data from various sources 
- **network/**: Network operations including creation, paths, neighborhoods
- **modify/**: Modules for modifying and curating pathway data
- **rpy2/**: Interfaces to R code
- **sbml_dfs_core.py, sbml_dfs_utils.py**: Core SBML dataframe functionality

### R Package (`lib/napistu-r/`)

- **R/**: R functions organized by module
  - **neighborhoods.R**: Functions for exploring network neighborhoods
  - **shortest_paths.R**: Functionality for pathway calculations
  - **netcontextr_*.R**: Core network analysis functionality
  - **module_*.R**: Shiny modules for interactive visualization

## Git Workflow

When contributing to Napistu:
1. Create a branch with the format `issue-{number}` from the main branch
2. Make your changes following the code conventions in `conventions.md`
3. Run tests to ensure they pass before submitting a PR
4. Create a pull request against the main branch

For automated issue fixes with Claude Code:
```bash
# Make sure you've authenticated with GitHub
gh auth login

# Run Claude Code to create a fix and PR
./utils/claude-pr.sh --main-repo=napistu/napistu --submodule=napistu-py --issue=42 --reviewer=username
```

## Code Conventions

- **Style**: Python (Black, Ruff) and R (Tidyverse)
- **Line length**: 100 characters
- **Indentation**: 2 spaces
- **Naming**: snake_case for variables and functions, PascalCase for classes
- **Documentation**: Public API methods require docstring comments
- **Testing**: Every public function requires at least one positive and one negative test

See `conventions.md` for detailed code conventions.