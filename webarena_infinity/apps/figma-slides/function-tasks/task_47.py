import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    template_styles = state.get("templateStyles", [])
    for ts in template_styles:
        if ts.get("id") == "ts_001":
            name = ts.get("name")
            if name == "Midnight Dark":
                return True, "Template style ts_001 name is correctly 'Midnight Dark'."
            else:
                return False, f"Template style ts_001 name is '{name}', expected 'Midnight Dark'."

    return False, "Template style ts_001 not found in state."
