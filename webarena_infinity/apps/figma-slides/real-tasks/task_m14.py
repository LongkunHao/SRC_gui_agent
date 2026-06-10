import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    libraries = state.get("libraries", [])

    if len(libraries) == 0:
        return False, "No libraries found in state"

    still_enabled = []
    for lib in libraries:
        if lib.get("enabled") is not False:
            still_enabled.append(lib.get("name", "Unknown"))

    if still_enabled:
        return False, f"Found {len(still_enabled)} library(ies) still enabled: {', '.join(still_enabled)}"

    return True, f"All {len(libraries)} libraries are disabled"
