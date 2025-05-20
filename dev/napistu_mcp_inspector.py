# Install the package in development mode if needed
# !pip install -e '.[mcp]'

import asyncio
import os
import sys
import logging
from pathlib import Path
import json

# Import the MCP components
from napistu.mcp.profiles import get_profile
from napistu.mcp.server import create_server, start_server

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("napistu")

# Create a dummy session context for execution components
session_context = {}
object_registry = {}

# define the types of assets to load
profile = get_profile("full")

mcp = create_server(profile)

# This is needed for the MCP Inspector to work
if __name__ == "__main__":
    mcp.run(start_server(mcp))