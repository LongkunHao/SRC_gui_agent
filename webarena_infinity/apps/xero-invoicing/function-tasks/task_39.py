import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    theme = next((t for t in state["brandingThemes"] if t["id"] == "theme_retail"), None)
    if not theme:
        return False, "Branding theme with id 'theme_retail' not found."

    if theme["name"] != "Retail Premium":
        return False, f"Theme name is '{theme['name']}', expected 'Retail Premium'."

    return True, "Retail branding theme renamed to 'Retail Premium'."
