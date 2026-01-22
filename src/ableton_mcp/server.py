"""MCP server for Ableton Live control.

Exposes tools for controlling Ableton Live via the Model Context Protocol.
"""

from fastmcp import FastMCP

from ableton_mcp.tools import register_all_tools

# Create FastMCP server
mcp = FastMCP("Ableton MCP Server")

# Register all tools from modular tool files
register_all_tools(mcp)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()
