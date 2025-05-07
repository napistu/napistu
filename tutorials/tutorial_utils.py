from __future__ import annotations

import logging
import os
import pathlib
import re
from os import PathLike
from typing import Optional
from subprocess import call
import yaml
from pydantic import BaseModel
from pydantic import ValidationError

from napistu import utils
from napistu.gcs import downloads

logger = logging.getLogger(__name__)

def locate_test_data() -> str:

    napistu_root = _find_napistu_root()
    _validate_git_submodules(napistu_root)

    test_data_path = os.path.join(
        napistu_root,
        "lib",
        "napistu-py",
        "src",
        "tests",
        "test_data"
        )

    if not os.path.isdir(test_data_path):
        raise FileNotFoundError(f"Test data was not located at the expected path {test_data_path}")
    
    return test_data_path


class NapistuConfig:

    """
    Configuration file for supporting notebooks

    Attributes
    ----------
    workflow: str
        The workflow to work with (same as the value of "workflow")
    config_dict: dict[str, Any]
        The configuration file directly read from yaml
    data_dir: str
        Path to the root directory where raw data and intermediate objects should be stored
    species_data_dir: str
        Path to species-specific data and results
    species: str
        The species name
    overwrite: bool
        Should intermediate data/objects be re-run (True) or re-used (False)
    artifacts: Optional[dict[str, str]]
        Artifacts relevant to "workflow"
    related: Optional[dict[str, Any]]
        Artifacts relevant to other "related_workflows".

    Methods
    -------
    deploy(server_name, connect_servers_settings)
        Create a new notebook on Posit Connect or update an existing one
    """

    def __init__(
        self,
        config_path: str | PathLike,
        workflow: str,
        related_workflows: list[str] | None = None,
    ) -> None:
        """
        Creates a NapistuConfig object to easily interact with a config file.

        Parameters
        ----------
        config_path (str)
            Path to a configuration .yaml file.
        workflow (str)
            Name of the workflow of interest. This should match one of the workflows
        in the config .yaml
        related_workflows (list(str) or None):
            an optional list of other named workflows. If provided these workflows will populate the
            "related_artifacts" attribute.

        Returns
        -------
        None.
        """

        self.workflow = workflow

        # read the .yaml config
        config_raw = self._read_config(config_path)

        # check whether the config is valid (and coerce it if possible)
        try:
            config_validated = _NapistuConfigValidator(**config_raw).model_dump()
        except ValidationError as e:
            logger.warning(e.errors())
            raise e

        self.config_dict = config_validated
        self.species = config_validated["global_vars"]["species"]
        self.overwrite = config_validated["global_vars"]["overwrite"]

        data_dir = os.path.expanduser(config_validated["global_vars"]["data_dir"])
        self.data_dir = data_dir
        self.species_data_dir = os.path.join(data_dir, re.sub(" ", "_", self.species))

        self.artifacts = self._format_workflow_artifacts(workflow)
        if self.artifacts is not None:
            for art in self.artifacts.values():
                self._create_artifact_dir(art)

        if related_workflows is not None:
            self.related = {x: self._format_workflow_artifacts(x) for x in related_workflows}  # type: ignore
        else:
            self.related = None  # type: ignore


    def deploy(self, server_name: str, connect_servers_settings: dict[str,str], venv_path: str|None = None) -> None:
        """Deploy a Jupyter Notebook to Posit Connect

        Args:
            server_name: str
                Name of the server running Posit Connect
            connect_servers_settings: dict[str, dict[str, str]]
                Dictionary of possible server names where values are dicts containing:
                    - url: the server's url
                    - pat_secret_name: the name environmental secret containing the PAT token
                        for deploying to Connect.
            venv_path: str
                The path to a virtual environment to use for rendering and deploying the notebook.

        Returns:
            None
        """

        workflow_settings = self.config_dict["workflows"][self.workflow]

        logger.debug(workflow_settings)

        deploy_notebook_connect(
            notebook_file=workflow_settings["name"],
            notebook_title=workflow_settings["title"],
            server_name=server_name,
            connect_servers_settings=connect_servers_settings,
            connect_id=workflow_settings["connect_id"],
            venv_path=venv_path
        )

        return None


    def load_asset(
        self,
        asset: str,
        subasset: str | None = None
        ) -> str:

        """
        Load Tutorial Asset

        Download the `asset` tutorial asset to `data_dir` if it doesn't
        already exist.

        asset: the file to download (which will be unpacked if its a .tar.gz)
        subasset: optional subasset bundled as part of the asset (if its an unpacked tar.gz)
        config: the tutorial configuation object

        """

        tutorial_init_msg = (
            "This appears to be the first time you've run a tutorial since a directory for"
            "storing tutorial data does not exist. This directory, defined by 'data_dir' "
            "in the globals sections of `config.yaml`, is currently set as {data_directory}.\n"
        )

        asset_path = downloads.load_public_napistu_asset(
            asset = asset,
            subasset = subasset,
            data_dir = self.data_dir,
            init_msg = tutorial_init_msg
        )
        
        return asset_path


    def _read_config(self, config_path: str | PathLike):
        if not os.path.isfile(config_path):
            raise FileNotFoundError(
                f"Configuration file not found with relative path: {config_path}"
            )

        config = dict()
        with open(config_path) as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.error(exc)

        return config


    def _format_workflow_artifacts(self, workflow: str):
        available_workflows = self.config_dict["workflows"].keys()
        if workflow not in available_workflows:
            raise ValueError(
                f"The provided workflow: {workflow} is not defined as a workflow in the config. "
                f"The named workflows are: {', '.join(available_workflows)}"
            )

        workflow_config = self.config_dict["workflows"][workflow]
        artifacts = workflow_config["artifacts"]
        if workflow_config["species_specific"]:
            workflow_data_dir = self.species_data_dir
        else:
            workflow_data_dir = self.data_dir

        if artifacts is None:
            return None
        else:
            return {
                k: os.path.join(workflow_data_dir, artifacts[k])
                for k in artifacts.keys()
            }


    def _create_artifact_dir(self, path: str) -> None:
        parentdir = os.path.dirname(path)
        if not os.path.isdir(parentdir):
            logger.info(f"Artifact directory not found; creating {parentdir}")
            pathlib.Path(parentdir).mkdir(parents=True, exist_ok=True)

        return None


def read_connect_settings(
    server_name: str, connect_servers_settings: dict[str, dict[str, str]]
) -> dict:
    """
    Read Connect Settings

    Validate server_settings and then pull out the settings for the selected server.

    Args:
        server_name: str
            Name of the server running Posit Connect
        connect_servers_settings: dict[str, dict[str, str]]
            Dictionary of possible server names where values are dicts containing:
                - url: the server's url
                - pat_secret_name: the name environmental secret containing the PAT token
                    for deploying to Connect.

    Returns:
        Dict containing server_name's parameters:
            server_url: str
                URL of the Connect server
            pat_secret_name: str
                Name of the environmental variable containing the Connect PAT
            connect_pat: str
                The PAT key associated with the "pat_secret_name" secret
    """

    # validate the provided server configs
    connect_configs = _ConnectConfigValidator(
        config=connect_servers_settings
    ).model_dump()["config"]

    if server_name not in connect_configs.keys():
        raise ValueError(
            f'The provide "server_name" {server_name} did not match any of the '
            f"configuations in \"connect_server_settings\": {' '.join(connect_configs.keys())}"
        )

    connect_settings = connect_configs[server_name]

    # add the server PAT key from an environmental variable
    connect_settings["connect_pat"] = read_environmental_variable(
        connect_settings["pat_secret_name"]
    )

    return connect_settings


def read_environmental_variable(envvar: str) -> str:
    if envvar not in os.environ.keys():
        raise ValueError(
            f"No environmental variable named {envvar} was found.\nPlease add this to your"
            ".bash_profile and reset your Jupyter sesion if you are working interactively"
        )

    return os.environ[envvar]


def deploy_notebook_connect(
    notebook_file: str,
    notebook_title: str,
    server_name: str,
    connect_servers_settings: dict[str, dict[str, str]],
    asset_type: str = "quarto",
    connect_id: str|None = None,
    venv_path: str|None = None
) -> None:
    """
    Deploy Notebook to Connect

    Publish a new or existing Jupyter notebook to Posit Connect.

    Args:
        notebook_file: str
            filename of the .ipynb
        notebook_title: str
            title of the to-be-published notebook
        server_name: str
            Name of the server running Posit Connect
        connect_servers_settings: dict[str, dict[str, str]]
            Dictionary of possible server names where values are dicts containing:
                - url: the server's url
                - pat_secret_name: the name environmental secret containing the PAT token
                    for deploying to Connect.
        asset_type: str
            The type of asset to deploy: e.g., "quarto" or "notebook"
        connect_id: str | None
            The Connect app ID of a previously published document or None to publish a new document
        venv_path: str
            If provided, the path to a virtual environment to use for rendering and deploying the notebook

    Returns:
        None

    """

    connect_settings = read_connect_settings(server_name, connect_servers_settings)

    arglist = [
        "rsconnect",
        "deploy",
        asset_type,
        "--title",
        f"'{notebook_title}'",
        "--server",
        f"'{connect_settings['url']}'",
        "--api-key",
        f"'{connect_settings['connect_pat']}'"
    ]

    if connect_id is None:
        logger.info("Publishing a new notebook to Connect")
        arglist = arglist + ["--new", notebook_file]
    else:
        logger.info("Updating an existing notebook on Connect")
        arglist = arglist + ["--app-id", connect_id, notebook_file]

    if venv_path is not None:
        arglist = ["source", f'{venv_path}/bin/activate', "&&"] + arglist

    print(f"Running command: {' '.join(arglist)}")
    
    call(" ".join(arglist), shell = True, executable='/bin/bash')

    return None


def _find_napistu_root():

    napistu_root, dirname = os.path.split(os.getcwd())

    if dirname != "tutorials":
        raise ValueError(f"The working directory basename was {dirname} when it should be \"Tutorials\". To locate the example data bundled with the project you should be working in napistu/tutorials")

    return napistu_root

def _validate_git_submodules(napistu_root):

    lib_dir = os.path.join(napistu_root, "lib")
    if not os.path.isdir(lib_dir):
        raise FileNotFoundError (f"The \"lib\" directory was not found within your napistu repo ({napistu_root})")

    EXPECTED_SUBMODULES = ["napistu-py", "napistu-r"]
    HELP_URL = "https://github.com/napistu/napistu/wiki/Environment-Setup#submodules"

    missing_submodules = [x for x in EXPECTED_SUBMODULES if not os.path.isdir(os.path.join(lib_dir, x))]

    if len(missing_submodules) > 0:
        raise ValueError(f"{len(missing_submodules)} submodules are missing from the lib directory: {', '.join(missing_submodules)}. See {HELP_URL}")

    return None


class _NapistuConfigValidator(BaseModel):
    global_vars: _NapistuConfigGlobalValidator
    workflows: dict[str, _NapistuConfigWorkflowValidator]


class _NapistuConfigGlobalValidator(BaseModel):
    data_dir: str
    species: str
    overwrite: bool


class _NapistuConfigWorkflowValidator(BaseModel):
    name: str
    title: str
    species_specific: bool
    connect_id: Optional[str]
    artifacts: Optional[dict[str, str]]


class _ConnectConfigValidator(BaseModel):
    config: dict[str, _ConnectServerValidator]


class _ConnectServerValidator(BaseModel):
    url: str
    pat_secret_name: str


