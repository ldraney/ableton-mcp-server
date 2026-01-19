"""OSC client singleton for Ableton connection."""

from abletonosc_client import connect, AbletonOSCClient

# Singleton client instance
_client: AbletonOSCClient | None = None


def get_client() -> AbletonOSCClient:
    """Get the shared OSC client instance.

    Creates a new client on first call, reuses it for subsequent calls.

    Returns:
        Connected AbletonOSCClient instance
    """
    global _client
    if _client is None:
        _client = connect()
    return _client


def reset_client() -> None:
    """Reset the client connection.

    Closes the current connection and clears the singleton.
    Next call to get_client() will create a new connection.
    """
    global _client
    if _client is not None:
        _client.close()
        _client = None
