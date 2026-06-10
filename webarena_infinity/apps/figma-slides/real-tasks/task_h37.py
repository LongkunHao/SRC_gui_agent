import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []
    deck = state.get("deckSettings", {})

    # Check available offline
    if deck.get("availableOffline") is not True:
        errors.append(f"availableOffline is {deck.get('availableOffline')}, expected True")

    # Check all libraries disabled
    for lib in state.get("libraries", []):
        if lib.get("enabled") is not False:
            errors.append(f"Library '{lib.get('name')}' is still enabled")

    # Check no Viewer collaborators remain
    for c in state.get("collaborators", []):
        if c.get("role") == "Viewer":
            errors.append(f"Viewer collaborator '{c.get('name')}' should have been removed")

    # Check slide number format is padded
    fmt = deck.get("slideNumberFormat")
    if fmt != "padded":
        errors.append(f"Slide number format is '{fmt}', expected 'padded'")

    if errors:
        return False, "; ".join(errors)
    return True, "Deck: offline enabled, all libraries disabled, Viewers removed, padded slide numbers"
