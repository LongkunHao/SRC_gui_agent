import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    libraries = state.get("libraries", [])

    # Library with most components is Presentation Icons Pack (320)
    # It should be disabled
    for lib in libraries:
        if lib.get("name") == "Presentation Icons Pack":
            if lib.get("enabled") is not False:
                errors.append("Presentation Icons Pack should be disabled")
            break

    # Library with pending updates is DesignCraft Component Library
    # It should be removed
    for lib in libraries:
        if lib.get("name") == "DesignCraft Component Library":
            errors.append(
                "DesignCraft Component Library should have been removed "
                "(it has pending updates)"
            )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Icons Pack disabled; DesignCraft library removed (had pending updates)"
