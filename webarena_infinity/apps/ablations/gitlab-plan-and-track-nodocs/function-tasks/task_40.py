import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    epic = next((e for e in state["epics"] if e["title"] == "Internationalization (i18n)"), None)
    if not epic:
        return False, "Epic 'Internationalization (i18n)' not found."

    if "multi-language" not in epic.get("description", "").lower():
        return False, f"Epic description does not contain expected text."

    if epic["status"] != "open":
        return False, f"Epic status is '{epic['status']}', expected 'open'."

    return True, "Epic 'Internationalization (i18n)' created successfully."
