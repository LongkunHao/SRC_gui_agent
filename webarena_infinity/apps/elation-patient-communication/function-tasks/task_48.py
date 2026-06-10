import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Torres (prov_2) virtual visit deactivated."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    providers = state.get("providers", [])

    provider = None
    for p in providers:
        if p.get("id") == "prov_2":
            provider = p
            break

    if provider is None:
        return False, "Provider prov_2 (Dr. Torres) not found in providers"

    if provider.get("virtualVisitActivated") is not False:
        return False, f"prov_2 virtualVisitActivated is {provider.get('virtualVisitActivated')}, expected False"

    return True, "Dr. Torres (prov_2) virtual visit correctly deactivated"
