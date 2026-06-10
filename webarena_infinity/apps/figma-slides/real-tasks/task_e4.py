import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    collaborators = state.get("collaborators", [])
    for collab in collaborators:
        if collab.get("name") == "Tom Nguyen":
            return False, "Tom Nguyen is still in the collaborators list"

    return True, "Tom Nguyen has been removed from collaborators"
