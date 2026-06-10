import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    libraries = state.get("libraries", [])
    for lib in libraries:
        if lib.get("id") == "lib_003" or lib.get("name") == "Presentation Icons Pack":
            enabled = lib.get("enabled")
            if enabled is False:
                return True, "Presentation Icons Pack (lib_003) is correctly disabled."
            else:
                return False, f"Presentation Icons Pack (lib_003) enabled is {enabled}, expected False."

    return False, "Library 'Presentation Icons Pack' (lib_003) not found in state."
