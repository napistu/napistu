# Napistu

The Napistu project is an approach for creating and working with genome-scale mechanistic networks. Pathways of interest can be created from multiple sources (e.g., Reactome, STRING, TRRUST), aggregated across sources, and refined to add additional information. This pathway representation can then be turned into a graphical network to identify molecular neighborhoods, find paths between molecules, and to carryout network propagation.

Napistu is an active project which we hope will be used for both simple analyses (e.g., basically replacing GSEA) as well as more complex analyses (e.g., multimodal data integration). 

With Napistu you can:

- Represent a range of publicly-available data sources using a common data structure, `sbml_dfs`, which is meant to faithfully encode molecular biology and biochemistry.
- Aggregate complementary sources into a consensus model which allows high-quality but incomplete interactions to be supported by data sources which more comprehensive yet speculative.
- Translate pathways models into geneome-scale graphical networks.

**Working with Pathways**

- Methods for visualizing pathways overlaid with experimental data.
- Methods for interacting with the underlying pathway networks.

This repository includes tutorials and documentation for the project while the following repositories contain the core packages:

- **[napistu-py](https://github.com/napistu/napistu-py)** - Napistu Python library: the core implementations of pathway representations and network-based searches.
  
[![PyPI version](https://badge.fury.io/py/napistu.svg)](https://badge.fury.io/py/napistu)
[![Documentation Status](https://readthedocs.org/projects/napistu/badge/?version=latest)](https://napistu.readthedocs.io/en/latest/?badge=latest)
[![CI](https://github.com/napistu/napistu-py/actions/workflows/ci.yml/badge.svg)](https://github.com/napistu/napistu-py/actions/workflows/ci.yml)
[![Release](https://github.com/napistu/napistu-py/actions/workflows/release.yml/badge.svg)](https://github.com/napistu/napistu-py/actions/workflows/release.yml)
[![Deploy to Cloud Run](https://github.com/napistu/napistu-py/actions/workflows/deploy.yml/badge.svg)](https://github.com/napistu/napistu-py/actions/workflows/deploy.yml)

- **[napistu-torch](https://github.com/napistu/napistu-torch)** - Napistu-Torch Python library: framework for applying graph neural networks to genome-scale pathways.

[![PyPI](https://badge.fury.io/py/napistu-torch.svg)](https://pypi.org/project/napistu-torch/)
[![Documentation](https://readthedocs.org/projects/napistu-torch/badge/?version=latest)](https://napistu-torch.readthedocs.io/)
[![CI](https://github.com/napistu/napistu-torch/actions/workflows/ci.yml/badge.svg)](https://github.com/napistu/napistu-torch/actions/workflows/ci.yml)
[![Release](https://github.com/napistu/napistu-torch/actions/workflows/release.yml/badge.svg)](https://github.com/napistu/napistu-torch/actions/workflows/release.yml)
 
- **[napistu-r](https://github.com/napistu/napistu-r)** - Napistu R library: R-based network visualization and a few utilities called from `napitsu-py`.

[![pkgdown site](https://github.com/napistu/napistu-r/actions/workflows/pkgdown.yaml/badge.svg)](https://napistu.github.io/napistu-r/)
[![R-CMD-check](https://github.com/napistu/napistu-r/actions/workflows/R-CMD-check-PR.yaml/badge.svg)](https://github.com/napistu/napistu-r/actions/workflows/R-CMD-check-PR.yaml)
[![pkgdown](https://github.com/napistu/napistu-r/actions/workflows/pkgdown.yaml/badge.svg)](https://github.com/napistu/napistu-r/actions/workflows/pkgdown.yaml)

# Using Napistu

## Tutorials

These tutorials are intended as stand-alone demonstrations of Napistu's core functionality. Most examples will focus on small pathways so that results can easily be reproduced by users.

- Downloading pathway data
- Understanding the `sbml_dfs` format
- Merging networks with the `consensus` module
- Using the CPR Command Line Interface (CLI)
- Formatting `sbml_dfs` as `napistu_graph` networks
- Suggesting mechanisms with network approaches
- Adding molecule- and reaction-level information to graphs
- R-based network visualization

## Examples

We'll include examples here of how Napistu is used in the wild to address biological questions. Stay tuned!

## Documentation

- For bug and issue tracking we use [Github Issues](https://github.com/napistu/napistu/issues).
- Napistu's core algorithms and data structures are documented on the [Napistu Wiki](https://github.com/napistu/napistu/wiki).

# Contributing to Napistu

- See `conventions.md` for an overview of Napistu's code conventions.
- Github Actions is used to test the individual R and Python repositories. Ensure that tests pass before contributing a pull request.
