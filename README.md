# Open-CPR

Landing zone for the Open source Calico Pathway Resources (CPR) project.

The Calico Pathway Resources (CPR) project is an approach for creating and working with genome-scale mechanistic networks. Pathways of interest can be created from multiple sources (e.g., Reactome, STRING, TRRUST), aggregated across sources, and refined to add additional information. This pathway representation can then be turned into a graphical network to identify molecular neighborhoods, find paths between molecules, and to carryout network propagation.

CPR is an active project which we hope will be used for both simple analyses (e.g., basically replacing GSEA) as well as more complex analyses (e.g., multimodal data integration). 

With CPR you can:

- Represent a range of publicly-available data sources using a common data structure, `sbml_dfs`, which is meant to faithfully encode molecular biology and biochemistry.
- Aggregate complementary sources into a consensus model which allows high-quality but incomplete interactions to be supported by data sources which more comprehensive yet speculative.
- Translate pathways models into geneome-scale graphical networks.

**Working with Pathways**

- Methods for visualizing pathways overlaid with experimental data.
- Methods for interacting with the underlying pathway networks.

This repository includes tutorials and documentation for the project while the following repositories contain the core packages:

- **calicolabs-open-cpr-py** - CPR Python library: the core implementations of pathway representations and network-based searches.
- **rcpr** - CPR R library: utilities supporting a few cpr functions and Shiny-based UI components for mechnet.

# Using CPR

## Tutorials

These tutorials are intended as stand-alone demonstrations of CPR's core functionality. Most examples will focus on small pathways so that results can easily be reproduced by users.

- Downloading pathway data
- Understanding the `sbml_dfs` format
- Merging networks with the `consensus` module
- Using the CPR Command Line Interface (CLI)
- Formatting `sbml_dfs` as `cpr_graph` networks
- Suggesting mechanisms with network approaches
- Adding molecule- and reaction-level information to graphs
- R-based network visualization

## Examples

We'll include examples here of how CPR is used in the wild to address biological questions. Stay tuned!

## Documentation

- For bug and issue tracking we use [Github Issues](https://github.com/calico/OpenCPR/issues).
- CPR's core algorithms and data structures are documented on the [CPR Wiki](https://github.com/calico/OpenCPR/wiki).
