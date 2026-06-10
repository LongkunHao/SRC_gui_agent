import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    theme = next((t for t in state["brandingThemes"] if t["id"] == "theme_standard"), None)
    if not theme:
        return False, "Standard branding theme not found."

    if theme["showTaxNumber"] is not False:
        return False, f"showTaxNumber is {theme['showTaxNumber']}, expected False."

    return True, "Standard theme showTaxNumber disabled."
