import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    share_settings = deck_settings.get("shareSettings", {})
    allow_download = share_settings.get("allowDownload")

    if allow_download is False:
        return True, "shareSettings.allowDownload is correctly set to False."
    else:
        return False, f"shareSettings.allowDownload is {allow_download}, expected False."
