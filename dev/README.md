# Dev Zone

This directory is meant to house functionality that should __NOT__ be needed by the majority of CPR users:
- workflows for creating and documenting assets stored in GCS

## GCS Assets

Since CPR primarily aims to gather, transform, and aggregate publically-available datasets we generally leave it to users to create pathway representations which are appropriate for their use cases. But, this is unduly painful when either publically-available data is not readily accessible or when we want to demonstrate and/or test functionality which depends on a complex series of upstream transformations. To deal with these issues we provide a modest number of the assets which can be downloaded from a public GoogleCloudStorage bucket. This is currently [Pathodex - open-cpr-prep](https://console.cloud.google.com/storage/browser/open_cpr_prep?project=calico-pathodex-03), but once open-sourced these assets will be moved to a bucket in [calico-public-data](https://console.cloud.google.com/storage/overview;tab=overview?project=calico-public-data). An overview of these assets follows:

- external_pathways:
    - `external_pathways_reactome_neo4j_members.csv`
        - groups of species with a common role (e.g., ligands of a receptor)
        - created by querying the Reactome Neo4J database using the ciphr query in `reactome_neo4j_queries.ipynb`
    - `external_pathways_reactome_neo4j_crossref.csv`
        - additional identifiers for Reactome species
        - created by querying the Reactome Neo4J database using the ciphr query in `reactome_neo4j_queries.ipynb`
    - (note: these files are not updated regularly and the process for folding this information into CPR is clearly suboptimal)

- pathways:
    - test.gz
        - a minimal pathway representation for quick testing.
        - created using the CPR CLI as shown in `test_pathway.qmd`.
    - human_consensus.gz
        - a human genome-scale physiological network integrating multiple data sources.
        - created using the CPR CLI as shown in `human_consensus.qmd`.
    - Each `pathway` bundles multiple files in a .tar.gz object. This includes:
        - `sbml_dfs.pkl` - the underlying pathway representation; an `SBML_dfs` object.
        - `identifiers.tsv` - a table containing systematic identifiers for the molecular species in the `sbml_dfs`.
        - 1+ graphs which translate the mechanisms described in `sbml_dfs` into edges in an (un)directed graph.
            - graph
            - distances - precomputed distances between pairs of molecular species. This greatly speeds up many of the network search algorithms.

## Environment Setup

```bash
uv venv --python 3.11
source .venv/bin/activate
pip install --upgrade pip wheel setuptools jupyter
# install the napistu python library from lib with support for rpy2
uv pip install '../lib/napistu-py[rpy2]'

python -m ipykernel install --name napistu_dev --display-name "Napistu - Dev" --user
```

## MCP Testing

- `napistu_mcp_inspector.py` runs a local MCP server. It can be run using:

```bash
python napistu_mcp_inspector.py
```

- To understand the contents of the MCP server we can look at it with:

```bash
# uv pip install "mcp[cli]"
mcp dev napistu_mcp_inspector.py
```
