# python napistu_mcp_inspector.py
# Install the package in development mode if needed
# !pip install -e '.[mcp]'

import asyncio
import os
import sys
import logging
from pathlib import Path
import json

from mcp.server.fastmcp.server import FastMCP

# Import the MCP components
from napistu.mcp.profiles import get_profile, ServerProfile
from napistu.mcp.server import create_server, initialize_components


# Set up logging
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger("napistu")

# Create a dummy session context for execution components
session_context = {}
object_registry = {}

# define the types of assets to load
profile: ServerProfile = get_profile("full", 
                                    session_context=session_context,
                                    object_registry=object_registry)

mcp: FastMCP = create_server(profile, host="127.0.0.1", port=8765)

# This is needed for the MCP Inspector to work
if __name__ == "__main__":
    """
    Main entry point for the MCP Inspector script.

    This script initializes all enabled MCP server components asynchronously, then starts the FastMCP server using streamable-http transport.
    """
    asyncio.run(initialize_components(mcp, profile))
    print("Initialization is complete!")
    
    # Debug: print registered MCP components
    print("Server settings:", mcp.settings)
    print("Profile config:", getattr(mcp, "profile_config", "Not found"))
    
    # Print available endpoints if possible
    if hasattr(mcp, "get_registered_endpoints"):
        print("Registered endpoints:")
        for endpoint in mcp.get_registered_endpoints():
            print(f" - {endpoint}")
    
    # Use the streamable-http transport with explicit parameters
    mcp.run(transport="streamable-http")
     