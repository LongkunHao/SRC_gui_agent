import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    libraries = state.get("libraries", [])

    for lib in libraries:
        if lib.get("id") == "lib_002" or lib.get("name") == "Brand Assets 2025":
            return False, "Library 'Brand Assets 2025' (lib_002) still exists, expected it to be removed."

    lib_count = len(libraries)
    if lib_count != 2:
        return False, f"Expected 2 libraries, found {lib_count}."

    return True, "Library 'Brand Assets 2025' has been removed and 2 libraries remain."
