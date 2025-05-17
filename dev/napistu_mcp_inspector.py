from mcp.server import FastMCP
import asyncio
import os

# Create a simple server for the inspector
server = FastMCP("napistu-inspector")

# Global data storage
_docs_cache = {
    "readme": {
        "README.md": "# Napistu\n\nThis is a sample README for testing with the MCP Inspector."
    }
}

# Register a resource
@server.resource("napistu://documentation/summary")
async def get_documentation_summary():
    """Get a summary of available documentation."""
    return {
        "readme_files": list(_docs_cache["readme"].keys())
    }

@server.resource("napistu://documentation/readme/{file_name}")
async def get_readme_content(file_name: str):
    """Get the content of a README file."""
    if file_name not in _docs_cache["readme"]:
        return {"error": f"README file {file_name} not found"}
    
    return {
        "content": _docs_cache["readme"][file_name],
        "format": "markdown"
    }

# Register a tool
@server.tool("search_documentation")
async def search_documentation(query: str):
    """Search documentation for a query."""
    results = {"readme": []}
    
    for name, content in _docs_cache["readme"].items():
        if query.lower() in content.lower():
            results["readme"].append({
                "name": name,
                "snippet": content[:100] + "..." if len(content) > 100 else content
            })
    
    return results

# This is needed for the MCP Inspector to work
if __name__ == "__main__":
    asyncio.run(server.run())