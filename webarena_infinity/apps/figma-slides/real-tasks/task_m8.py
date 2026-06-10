import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    collaborators = state.get("collaborators", [])

    viewers = []
    for c in collaborators:
        if c.get("role") == "Viewer":
            viewers.append(c.get("name", "Unknown"))

    if viewers:
        return False, f"Found {len(viewers)} Viewer collaborator(s) still present: {', '.join(viewers)}"

    if len(collaborators) == 0:
        return False, "No collaborators found at all - all collaborators were removed instead of just Viewers"

    return True, f"All Viewer collaborators removed, {len(collaborators)} non-Viewer collaborators remain"
