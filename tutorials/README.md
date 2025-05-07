This directory contains notebooks demonstrating how individual data sources can be downloaded and formatted

Each notebook reads from a common config file, config.yaml, containing global variables which are available in all notebooks as well as workflow-specific variables. The notebook naming conventions highlight whether notebooks can be run from scratch or depend on artifacts generated in upstream notebooks.

- Notebooks starting with a (1) can be run from scratch - they will download and organize any information needed.
- Notebooks starting with (2+) require some upstream files - paths to these artifacts are specified as related_workflows arguments to configs.CprConfig.

A few notebooks have a special role:

- 0_run_and_deploy_all.ipynb - this jupyter notebook can be used to run multiple notebooks and deploy the resulting html to Posit Connect.
- 1_workflow_cpr_cli.qmd - this notebook uses the CPR CLI to create a multiple source pathway representation. This is useful both to demonstrate the preferred way for generating analysis-ready artifacts, but also to highlight the clear input-output relationships of individual steps which are suitable for integration into a workflow manager. At Calico, these steps are executed through Cloud Composer as part of Pathadex.

## Environment Setup

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install --upgrade pip wheel setuptools ipykernel jupyter
# install the cpr python library from lib with support for rpy2
uv pip install '../lib/napistu-py[rpy2]'
# install runtime dependencies
uv pip install pycairo

python -m ipykernel install --name napistu_tutorials --display-name "Napistu - Tutorials" --user
```
