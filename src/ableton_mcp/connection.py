"""OSC client singleton for Ableton connection."""

import os
import threading

from abletonosc_client import connect, AbletonOSCClient

# Singleton client instance with thread-safe lock
_client: AbletonOSCClient | None = None
_lock = threading.Lock()

# Configuration via environment variables
# For WSL2: ABLETON_HOST=172.25.128.1 (or use auto-detect)
# ABLETON_LISTEN_HOST=0.0.0.0 for WSL2->Windows
ABLETON_HOST = os.environ.get("ABLETON_HOST", "127.0.0.1")
ABLETON_LISTEN_HOST = os.environ.get("ABLETON_LISTEN_HOST")


def _detect_wsl2_host() -> tuple[str, str | None]:
    """Detect if running in WSL2 and return appropriate host settings."""
    # Check if running in WSL2
    try:
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                # Running in WSL2 - get Windows host from default gateway
                import subprocess
                result = subprocess.run(
                    ["ip", "route", "show", "default"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    # Parse: "default via 172.25.128.1 dev eth0 ..."
                    parts = result.stdout.split()
                    if len(parts) >= 3 and parts[0] == "default":
                        windows_host = parts[2]
                        return (windows_host, "0.0.0.0")
    except Exception:
        pass
    return (ABLETON_HOST, ABLETON_LISTEN_HOST)


def get_client() -> AbletonOSCClient:
    """Get the shared OSC client instance.

    Creates a new client on first call, reuses it for subsequent calls.
    Thread-safe to prevent "Address already in use" errors when
    multiple tools are called in parallel.

    Auto-detects WSL2 and configures Windows host accordingly.

    Returns:
        Connected AbletonOSCClient instance
    """
    global _client
    if _client is None:
        with _lock:
            # Double-check after acquiring lock
            if _client is None:
                host, listen_host = _detect_wsl2_host()
                _client = connect(host=host, listen_host=listen_host)
    return _client


def reset_client() -> None:
    """Reset the client connection.

    Closes the current connection and clears the singleton.
    Next call to get_client() will create a new connection.
    Thread-safe.
    """
    global _client
    with _lock:
        if _client is not None:
            _client.close()
            _client = None
