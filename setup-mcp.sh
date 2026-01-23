#!/bin/bash
# Generate .mcp.json from template with the current directory and Python paths

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Get the Python path from Poetry virtualenv
PYTHON_PATH=$(poetry env info --executable 2>/dev/null)
if [ -z "$PYTHON_PATH" ]; then
    echo "Error: Could not find Poetry virtualenv. Run 'poetry install' first."
    exit 1
fi

sed -e "s|{{ABLETON_MCP_PATH}}|$SCRIPT_DIR|g" \
    -e "s|{{PYTHON_PATH}}|$PYTHON_PATH|g" \
    "$SCRIPT_DIR/.mcp.json.template" > "$SCRIPT_DIR/.mcp.json"

echo "Generated .mcp.json:"
echo "  Python: $PYTHON_PATH"
echo "  Path: $SCRIPT_DIR"
echo ""
echo "Restart Claude Code to pick up the MCP server."
