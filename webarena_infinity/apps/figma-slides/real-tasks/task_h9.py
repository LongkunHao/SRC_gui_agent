import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Check no collaborator with role == "Viewer"
    collaborators = state.get("collaborators", [])
    viewers = []
    for c in collaborators:
        role = c.get("role", "")
        if role.lower() == "viewer":
            viewers.append(c.get("name", c.get("id", "unknown")))

    if viewers:
        errors.append(f"Viewer collaborators still present: {', '.join(viewers)}")

    # Check share settings
    share = state.get("shareSettings", state.get("deckSettings", {}).get("shareSettings", {}))
    if not share:
        # Try nested in deckSettings
        deck = state.get("deckSettings", {})
        share = deck.get("shareSettings", {})

    link_access = share.get("linkAccess", "")
    if link_access != "restricted":
        errors.append(f"linkAccess is '{link_access}', expected 'restricted'")

    allow_copy = share.get("allowCopy")
    if allow_copy is not False:
        errors.append(f"allowCopy is {allow_copy}, expected False")

    allow_download = share.get("allowDownload")
    if allow_download is not False:
        errors.append(f"allowDownload is {allow_download}, expected False")

    if errors:
        return False, "; ".join(errors)
    return True, "Viewer collaborators removed, link access restricted, copy and download disabled"
