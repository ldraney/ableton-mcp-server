"""Application tools for the Ableton MCP server.

Covers application-level operations like version info, connection testing, and messaging.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Application


def register_application_tools(mcp):
    """Register all application tools with the MCP server."""

    @mcp.tool()
    def application_test(
        timeout: Annotated[float, Field(description="How long to wait for response in seconds", gt=0)] = 2.0
    ) -> bool:
        """Test the connection to AbletonOSC.

        Args:
            timeout: How long to wait for response in seconds (default: 2.0)

        Returns:
            True if connection is working
        """
        app = Application(get_client())
        return app.test(timeout)

    @mcp.tool()
    def application_get_version() -> str:
        """Get the Ableton Live version string.

        Returns:
            Version string (e.g., "12.0.1")
        """
        app = Application(get_client())
        return app.get_version()

    @mcp.tool()
    def application_get_api_version() -> int:
        """Get the AbletonOSC API version.

        Returns:
            API version number
        """
        app = Application(get_client())
        return app.get_api_version()

    @mcp.tool()
    def application_reload() -> str:
        """Reload the AbletonOSC MIDI Remote Script.

        Useful for development when editing the script without restarting Ableton.

        Returns:
            Confirmation message
        """
        app = Application(get_client())
        app.reload()
        return "AbletonOSC script reloaded"

    @mcp.tool()
    def application_get_log_level() -> str:
        """Get the AbletonOSC log level.

        Returns:
            Log level: "debug", "info", "warning", "error", or "critical"
        """
        app = Application(get_client())
        return app.get_log_level()

    @mcp.tool()
    def application_set_log_level(
        level: Annotated[str, Field(description="Log level ('debug', 'info', 'warning', 'error', 'critical')")]
    ) -> str:
        """Set the AbletonOSC log level.

        Args:
            level: Log level ("debug", "info", "warning", "error", "critical")

        Returns:
            Confirmation message
        """
        app = Application(get_client())
        app.set_log_level(level)
        return f"Log level set to {level}"

    @mcp.tool()
    def application_show_message(
        message: Annotated[str, Field(description="Message to display in Ableton's status bar")]
    ) -> str:
        """Display a message in Ableton's status bar.

        Args:
            message: Message to display

        Returns:
            Confirmation message
        """
        app = Application(get_client())
        app.show_message(message)
        return f"Message displayed: {message}"
