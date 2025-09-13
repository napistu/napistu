This directory contains notebooks demonstrating how individual data sources can be downloaded and formatted

Each notebook reads from a common config file, config.yaml, containing global variables which are available in all notebooks as well as workflow-specific variables.

## Environment Setup

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install --upgrade pip wheel setuptools ipykernel jupyter
# install the napistu python library from lib with support for rpy2
uv pip install '../lib/napistu-py[rpy2]'
# install runtime dependencies
uv pip install pycairo seaborn

python -m ipykernel install --name napistu_tutorials --display-name "Napistu - Tutorials"
```
