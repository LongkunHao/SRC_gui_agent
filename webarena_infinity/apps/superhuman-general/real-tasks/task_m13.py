import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Shipping Update" auto label
    target_auto_label = None
    for al in state.get("autoLabels", []):
        if al.get("name") == "Shipping Update":
            target_auto_label = al
            break

    if not target_auto_label:
        return False, "Could not find auto label 'Shipping Update' in state."

    # Check that it is disabled (enabled == False)
    if target_auto_label.get("enabled") == False:
        return True, "Auto label 'Shipping Update' is disabled."
    else:
        return False, f"Auto label 'Shipping Update' is still enabled. enabled: {target_auto_label.get('enabled')}"
