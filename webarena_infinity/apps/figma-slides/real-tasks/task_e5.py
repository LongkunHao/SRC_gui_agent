import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    libraries = state.get("libraries", [])
    target = None
    for lib in libraries:
        if lib.get("name") == "Presentation Icons Pack":
            target = lib
            break

    if target is None:
        return False, "Could not find library 'Presentation Icons Pack'"

    if target.get("enabled") is not False:
        return False, f"Presentation Icons Pack is still enabled (enabled={target.get('enabled')})"

    return True, "Presentation Icons Pack library is disabled"
