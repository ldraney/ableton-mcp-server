"""Browser tools for the Ableton MCP server.

Provides tools for exploring Ableton's browser, listing packs,
and searching for devices/presets across all installed content.
"""

from typing import Annotated, List

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Browser


def register_browser_tools(mcp):
    """Register all browser tools with the MCP server."""

    # =============================================================================
    # Pack Exploration (via Ableton API - limited functionality)
    # =============================================================================

    @mcp.tool()
    def browser_list_packs() -> List[str]:
        """List all installed Ableton pack names.

        Returns a list of all packs visible in Ableton's browser,
        including Core Library, Session Drums, and any purchased packs.

        Returns:
            List of pack names
        """
        browser = Browser(get_client())
        return browser.list_packs()

    @mcp.tool()
    def browser_list_pack_contents(
        pack_name: Annotated[str, Field(description="Name of the pack to explore (can be partial match)")],
        max_depth: Annotated[int, Field(description="Maximum folder depth to search", ge=1, le=20)] = 10
    ) -> List[str]:
        """List all loadable items in a pack.

        Recursively explores a pack and returns paths to all loadable
        items (presets, instruments, effects, drum kits, etc.).

        Args:
            pack_name: Name of the pack to explore (can be partial match)
            max_depth: Maximum folder depth to search (default: 10)

        Returns:
            List of item paths (e.g., "Pack/Instruments/Keys/Piano.adv")
        """
        browser = Browser(get_client())
        return browser.list_pack_contents(pack_name, max_depth)

    # =============================================================================
    # Search
    # =============================================================================

    @mcp.tool()
    def browser_search(
        query: Annotated[str, Field(description="Search string (case-insensitive partial match)")],
        max_results: Annotated[int, Field(description="Maximum number of results", ge=1, le=200)] = 50,
        max_depth: Annotated[int, Field(description="Maximum folder depth to search", ge=1, le=20)] = 10
    ) -> List[dict]:
        """Search all packs for items matching a query.

        Performs a recursive search through all installed packs to find
        instruments, effects, presets, and drum kits matching the query.

        This is useful for discovering what devices are available before
        using track_insert_device to load them.

        Args:
            query: Search string (case-insensitive partial match)
            max_results: Maximum number of results to return (default: 50)
            max_depth: Maximum folder depth to search (default: 10)

        Returns:
            List of dicts with item_name, pack_name, and full_path
        """
        browser = Browser(get_client())
        results = browser.search(query, max_results, max_depth)
        return [
            {"item_name": name, "pack_name": pack, "full_path": path}
            for name, pack, path in results
        ]

    @mcp.tool()
    def browser_search_and_load(
        query: Annotated[str, Field(description="Search string (case-insensitive partial match)")]
    ) -> str:
        """Search for an item and load the first match.

        Searches all packs and standard browser locations for an item
        matching the query. If found, loads it into the currently
        selected track.

        This is a convenience function that combines search + load.
        For more control, use browser_search to find items first,
        then track_insert_device to load a specific one.

        Args:
            query: Search string (case-insensitive partial match)

        Returns:
            Name of the loaded item, or message if not found
        """
        browser = Browser(get_client())
        result = browser.search_and_load(query)
        if result:
            return f"Loaded: {result}"
        else:
            return f"No item found matching '{query}'"

    @mcp.tool()
    def browser_search_by_type(
        query: Annotated[str, Field(description="Search string (case-insensitive partial match)")],
        device_type: Annotated[str, Field(description="Category to search: 'instrument', 'audio_effect', 'midi_effect', or 'drums'")]
    ) -> List[str]:
        """Search for devices within a specific category only.

        This is faster than browser_search because it only searches
        one category. Useful when you know what type of device you want.

        Args:
            query: Search string (case-insensitive partial match)
            device_type: Category to search:
                         'instrument', 'audio_effect', 'midi_effect', 'drums'

        Returns:
            List of matching device names
        """
        browser = Browser(get_client())

        valid_types = ['instrument', 'audio_effect', 'midi_effect', 'drums']
        if device_type not in valid_types:
            return [f"Invalid device_type: '{device_type}'. Must be one of: {valid_types}"]

        # Get items from the specified category
        if device_type == 'instrument':
            items = browser.list_instruments()
        elif device_type == 'audio_effect':
            items = browser.list_audio_effects()
        elif device_type == 'midi_effect':
            items = browser.list_midi_effects()
        elif device_type == 'drums':
            items = browser.list_drums()

        # Find fuzzy matches (case-insensitive)
        query_lower = query.lower()
        matches = [item for item in items if query_lower in item.lower()]

        return matches

    # =============================================================================
    # Loading Items
    # =============================================================================

    @mcp.tool()
    def browser_load_item(
        full_path: Annotated[str, Field(description="Full path to the item (e.g., 'Pack/Folder/Item')")]
    ) -> str:
        """Load a browser item by its full path.

        The path should be in the format returned by browser_list_pack_contents
        or browser_search, e.g., "Electric Keyboards/Sounds/Suitcase Piano/Default"

        Args:
            full_path: Full path to the item

        Returns:
            Confirmation message
        """
        browser = Browser(get_client())
        success = browser.load_item(full_path)
        if success:
            return f"Successfully loaded: {full_path}"
        else:
            return f"Failed to load: {full_path}"

    # =============================================================================
    # Standard Browser Locations
    # =============================================================================

    @mcp.tool()
    def browser_list_instruments() -> List[str]:
        """List top-level items in the instruments browser.

        Returns the names of instruments and folders visible in
        Ableton's Instruments browser section.

        Returns:
            List of instrument names/folder names
        """
        browser = Browser(get_client())
        return browser.list_instruments()

    @mcp.tool()
    def browser_list_audio_effects() -> List[str]:
        """List top-level items in the audio effects browser.

        Returns the names of audio effects and folders visible in
        Ableton's Audio Effects browser section.

        Returns:
            List of audio effect names/folder names
        """
        browser = Browser(get_client())
        return browser.list_audio_effects()

    @mcp.tool()
    def browser_list_midi_effects() -> List[str]:
        """List top-level items in the MIDI effects browser.

        Returns the names of MIDI effects visible in Ableton's
        MIDI Effects browser section.

        Returns:
            List of MIDI effect names/folder names
        """
        browser = Browser(get_client())
        return browser.list_midi_effects()

    @mcp.tool()
    def browser_list_drums() -> List[str]:
        """List top-level items in the drums browser.

        Returns the names of drum kits and folders visible in
        Ableton's Drums browser section.

        Returns:
            List of drum kit names/folder names
        """
        browser = Browser(get_client())
        return browser.list_drums()

    @mcp.tool()
    def browser_list_sounds() -> List[str]:
        """List top-level items in the sounds browser.

        Returns the names of sounds and folders visible in
        Ableton's Sounds browser section.

        Returns:
            List of sound names/folder names
        """
        browser = Browser(get_client())
        return browser.list_sounds()
