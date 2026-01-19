"""OSC client singleton for Ableton connection."""

import threading

from abletonosc_client import connect, AbletonOSCClient

# Singleton client instance with thread-safe lock
_client: AbletonOSCClient | None = None
_lock = threading.Lock()


def get_client() -> AbletonOSCClient:
    """Get the shared OSC client instance.

    Creates a new client on first call, reuses it for subsequent calls.
    Thread-safe to prevent "Address already in use" errors when
    multiple tools are called in parallel.

    Returns:
        Connected AbletonOSCClient instance
    """
    global _client
    if _client is None:
        with _lock:
            # Double-check after acquiring lock
            if _client is None:
                _client = connect()
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
