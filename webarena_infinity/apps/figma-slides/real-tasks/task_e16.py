import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    libraries = state.get("libraries", [])
    for lib in libraries:
        if lib.get("name") == "Brand Assets 2025":
            return False, "Brand Assets 2025 library still exists"

    return True, "Brand Assets 2025 library has been removed"
