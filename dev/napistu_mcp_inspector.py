# Install the package in development mode if needed
# !pip install -e '.[mcp]'

import asyncio
import os
import sys
import logging
from pathlib import Path
import json

# Import the MCP components
from napistu.mcp.profiles import get_profile, ServerProfile
from napistu.mcp.server import create_server, initialize_components
from mcp.server.fastmcp.server import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("napistu")

# Create a dummy session context for execution components
session_context = {}
object_registry = {}

# define the types of assets to load
profile: ServerProfile = get_profile("full")
mcp: FastMCP = create_server(profile)

# This is needed for the MCP Inspector to work
if __name__ == "__main__":
    """
    Main entry point for the MCP Inspector script.

    This script initializes all enabled MCP server components asynchronously, then starts the FastMCP server using stdio transport.
    """
    asyncio.run(initialize_components(mcp))
    print("Initialization is complete!")
    mcp.run("streamable-http")