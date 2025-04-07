This directory contains notebooks demonstrating how individual data sources can be downloaded and formatted

Each notebook reads from a common config file, config.yaml, containing global variables which are available in all notebooks as well as workflow-specific variables. The notebook naming conventions highlight whether notebooks can be run from scratch or depend on artifacts generated in upstream notebooks.

- Notebooks starting with a (1) can be run from scratch - they will download and organize any information needed.
- Notebooks starting with (2+) require some upstream files - paths to these artifacts are specified as related_workflows arguments to configs.CprConfig.

A few notebooks have a special role:

- 0_run_and_deploy_all.ipynb - this jupyter notebook can be used to run multiple notebooks and deploy the resulting html to Posit Connect.
- 1_workflow_cpr_cli.qmd - this notebook uses the CPR CLI to create a multiple source pathway representation. This is useful both to demonstrate the preferred way for generating analysis-ready artifacts, but also to highlight the clear input-output relationships of individual steps which are suitable for integration into a workflow manager. At Calico, these steps are executed through Cloud Composer as part of Pathadex.

## Environment Setup

```bash
# create a venv using an appropriate Python binary - /env is used because it is
# recognized by Quarto: https://quarto.org/docs/projects/virtual-environments.html
python -m venv env
source env/bin/activate
pip install --upgrade pip wheel setuptools ipykernel jupyter
# install the cpr python library from lib with support for rpy2
pip install ../lib/calicolabs-open-cpr-py[rpy2]
# install runtime dependencies
pip install pycairo

python -m ipykernel install --name open_cpr_tutorials --display-name "Open CPR - Tutorials" --user
```
