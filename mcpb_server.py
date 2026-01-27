#!/usr/bin/env python3
"""MCPB entry point - thin wrapper that runs the ableton-mcp server.

NOTE: This bundle requires ableton-mcp-server to be published on PyPI.
Currently it has a git dependency on abletonosc-client which prevents PyPI publishing.
"""

from ableton_mcp.server import main

if __name__ == "__main__":
    main()
