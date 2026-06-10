import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # In seed data, online Editors: Marcus Rivera, Aiko Tanaka, David Park
    online_editor_names = {"Marcus Rivera", "Aiko Tanaka", "David Park"}

    for c in state.get("collaborators", []):
        name = c.get("name", "")
        if name in online_editor_names:
            role = c.get("role")
            if role != "Viewer":
                errors.append(f"'{name}' role is '{role}', expected 'Viewer'")

    # No resolved comments should remain
    for c in state.get("comments", []):
        if c.get("resolved") is True:
            errors.append(f"Resolved comment '{c.get('id')}' should have been deleted")

    if errors:
        return False, "; ".join(errors)
    return True, "Online Editors downgraded to Viewer; all resolved comments deleted"
