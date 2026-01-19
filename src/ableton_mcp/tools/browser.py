"""Browser tools for the Ableton MCP server.

Provides tools for exploring Ableton's browser, listing packs,
and searching for devices/presets across all installed content.
"""

import json
import os
from datetime import datetime
from typing import Annotated, List

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Browser


def register_browser_tools(mcp):
    """Register all browser tools with the MCP server."""

    # =============================================================================
    # Filesystem Pack Discovery (workaround for browser.packs API returning empty)
    # =============================================================================

    @mcp.tool()
    def browser_scan_packs_from_disk(
        pack_root: Annotated[str, Field(description="Root directory for packs (default: ~/Music/Ableton/Factory Packs)")] = ""
    ) -> dict:
        """Scan filesystem to enumerate installed packs and their .adg files.

        Since browser.packs API returns empty, this tool scans the filesystem
        at ~/Music/Ableton/Factory Packs/ to discover all installed packs
        and their loadable .adg (Ableton Device Group) files.

        This is the recommended way to discover what packs are installed
        and what presets they contain.

        Args:
            pack_root: Root directory for packs (default: ~/Music/Ableton/Factory Packs)

        Returns:
            Dict mapping pack names to lists of .adg files found in each pack
        """
        if not pack_root:
            pack_root = os.path.expanduser("~/Music/Ableton/Factory Packs")

        if not os.path.isdir(pack_root):
            return {"error": f"Pack directory not found: {pack_root}"}

        packs = {}
        for pack_name in os.listdir(pack_root):
            pack_path = os.path.join(pack_root, pack_name)
            if os.path.isdir(pack_path):
                # Find all .adg files recursively
                adg_files = []
                for root, dirs, files in os.walk(pack_path):
                    for f in files:
                        if f.endswith('.adg'):
                            # Store relative path from pack root
                            rel_path = os.path.relpath(os.path.join(root, f), pack_path)
                            adg_files.append(rel_path)
                if adg_files:  # Only include packs with .adg files
                    packs[pack_name] = sorted(adg_files)

        return packs

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

    @mcp.tool()
    def browser_search_in_packs(
        query: Annotated[str, Field(description="Search string (case-insensitive partial match)")],
        pack_names: Annotated[List[str], Field(description="List of pack names to search (fuzzy match)")] = None
    ) -> List[dict]:
        """Search for devices within specific packs (filesystem scan).

        Scans the filesystem at ~/Music/Ableton/Factory Packs/
        for .adg files matching the query. This is useful for finding
        presets in specific packs.

        Args:
            query: Search string (case-insensitive partial match)
            pack_names: List of pack names to search. If None, searches all packs.

        Returns:
            List of dicts with device_name, pack_name, and relative_path
        """
        pack_root = os.path.expanduser("~/Music/Ableton/Factory Packs")
        if not os.path.isdir(pack_root):
            return [{"error": f"Pack directory not found: {pack_root}"}]

        results = []
        query_lower = query.lower()

        # Get list of packs to search
        all_packs = [p for p in os.listdir(pack_root)
                     if os.path.isdir(os.path.join(pack_root, p))]

        if pack_names:
            # Filter to specified packs (fuzzy match)
            packs_to_search = []
            for target_pack in pack_names:
                target_lower = target_pack.lower()
                for pack in all_packs:
                    if target_lower in pack.lower() and pack not in packs_to_search:
                        packs_to_search.append(pack)
        else:
            packs_to_search = all_packs

        # Search each pack
        for pack_name in packs_to_search:
            pack_path = os.path.join(pack_root, pack_name)
            for root, dirs, files in os.walk(pack_path):
                for f in files:
                    if f.endswith('.adg') and query_lower in f.lower():
                        rel_path = os.path.relpath(os.path.join(root, f), pack_path)
                        results.append({
                            "device_name": f,
                            "pack_name": pack_name,
                            "relative_path": rel_path
                        })

        return results

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

    # =============================================================================
    # Local Browser Cache Generation
    # =============================================================================

    @mcp.tool()
    def browser_generate_local_cache(
        output_path: Annotated[str, Field(description="Path to write the cache file (default: ./local_browser_cache.json)")] = ""
    ) -> str:
        """Generate a local cache of all browser content.

        Enumerates all items from standard browser locations and saves
        them to a JSON file. This creates a local registry of available
        devices that can be used for quick lookups.

        The generated file should be added to .gitignore as it represents
        local Ableton configuration.

        File extensions:
        - .adg = Ableton Device Group (drum racks, instrument racks, presets)
        - .adv = Ableton Device Preset
        - .als = Ableton Live Set
        - .alc = Ableton Live Clip

        Args:
            output_path: Where to save the cache (default: ./local_browser_cache.json)

        Returns:
            Confirmation message with stats
        """
        browser = Browser(get_client())

        # Collect all browser content
        cache = {
            "generated_at": datetime.now().isoformat(),
            "description": "Auto-generated browser cache. Add to .gitignore.",
            "browser": {
                "instruments": browser.list_instruments(),
                "audio_effects": browser.list_audio_effects(),
                "midi_effects": browser.list_midi_effects(),
                "drums": browser.list_drums(),
                "sounds": browser.list_sounds(),
            },
            "loadable_items": {},
            "search_terms": {}
        }

        # Process drums - these are directly loadable .adg files
        for item in cache["browser"]["drums"]:
            if item.endswith(".adg"):
                # Extract search term (name without extension)
                name = item[:-4]  # Remove .adg
                # Create variations for search
                search_term = name.replace(" Kit", "").replace(".adg", "")
                cache["loadable_items"][item] = {
                    "category": "drums",
                    "name": name,
                    "search_terms": [name, search_term]
                }
                # Index by search terms
                for term in [name.lower(), search_term.lower()]:
                    if term not in cache["search_terms"]:
                        cache["search_terms"][term] = []
                    cache["search_terms"][term].append(item)

        # Process instruments - these are folder names
        for item in cache["browser"]["instruments"]:
            cache["loadable_items"][item] = {
                "category": "instruments",
                "name": item,
                "type": "folder" if not item.endswith((".adg", ".adv")) else "preset",
                "search_terms": [item]
            }

        # Process audio effects
        for item in cache["browser"]["audio_effects"]:
            cache["loadable_items"][item] = {
                "category": "audio_effects",
                "name": item,
                "type": "folder" if not item.endswith((".adg", ".adv")) else "preset",
                "search_terms": [item]
            }

        # Process MIDI effects
        for item in cache["browser"]["midi_effects"]:
            cache["loadable_items"][item] = {
                "category": "midi_effects",
                "name": item,
                "type": "folder" if not item.endswith((".adg", ".adv")) else "preset",
                "search_terms": [item]
            }

        # Scan packs from disk (workaround for browser.packs API)
        pack_root = os.path.expanduser("~/Music/Ableton/Factory Packs")
        packs_from_disk = {}
        total_pack_presets = 0
        if os.path.isdir(pack_root):
            for pack_name in os.listdir(pack_root):
                pack_path = os.path.join(pack_root, pack_name)
                if os.path.isdir(pack_path):
                    adg_files = []
                    for root, dirs, files in os.walk(pack_path):
                        for f in files:
                            if f.endswith('.adg'):
                                rel_path = os.path.relpath(os.path.join(root, f), pack_path)
                                adg_files.append(rel_path)
                                # Add to search terms
                                name_without_ext = f[:-4]  # Remove .adg
                                search_key = name_without_ext.lower()
                                if search_key not in cache["search_terms"]:
                                    cache["search_terms"][search_key] = []
                                cache["search_terms"][search_key].append(f"{pack_name}/{rel_path}")
                    if adg_files:
                        packs_from_disk[pack_name] = sorted(adg_files)
                        total_pack_presets += len(adg_files)

        cache["packs_from_disk"] = packs_from_disk

        # Determine output path
        if not output_path:
            # Default to project root
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
                "local_browser_cache.json"
            )

        # Write cache
        with open(output_path, "w") as f:
            json.dump(cache, f, indent=2)

        # Stats
        total_loadable = len([i for i in cache["browser"]["drums"] if i.endswith(".adg")])
        total_instruments = len(cache["browser"]["instruments"])
        total_effects = len(cache["browser"]["audio_effects"]) + len(cache["browser"]["midi_effects"])
        num_packs = len(packs_from_disk)

        return (
            f"Generated browser cache at: {output_path}\n"
            f"- Drum kits (.adg): {total_loadable}\n"
            f"- Instruments: {total_instruments}\n"
            f"- Effects: {total_effects}\n"
            f"- Sound categories: {len(cache['browser']['sounds'])}\n"
            f"- Packs from disk: {num_packs} packs, {total_pack_presets} presets (.adg)\n"
            f"Remember to add 'local_browser_cache.json' to .gitignore"
        )
