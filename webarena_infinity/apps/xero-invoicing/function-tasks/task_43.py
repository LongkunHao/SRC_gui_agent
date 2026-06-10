import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    theme = next((t for t in state["brandingThemes"] if t["id"] == "theme_professional"), None)
    if not theme:
        return False, "Professional Services branding theme not found."

    expected = "All work is subject to our Master Services Agreement. Payment terms are strictly net 30 days."
    if theme["termsAndConditions"] != expected:
        return False, f"Terms and conditions don't match expected value."

    return True, "Professional Services theme terms and conditions updated."
