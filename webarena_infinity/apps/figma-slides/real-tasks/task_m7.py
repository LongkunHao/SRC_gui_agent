import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    share_settings = deck_settings.get("shareSettings", {})

    allow_copy = share_settings.get("allowCopy")
    allow_download = share_settings.get("allowDownload")

    errors = []
    if allow_copy is not False:
        errors.append(f"allowCopy is {allow_copy}, expected False")
    if allow_download is not False:
        errors.append(f"allowDownload is {allow_download}, expected False")

    if errors:
        return False, "; ".join(errors)

    return True, "Copy and download are both disabled in share settings"
