import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Chen (prov_1) sharing default changed to 3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    providers = state.get("providers", [])

    provider = None
    for p in providers:
        if p.get("id") == "prov_1":
            provider = p
            break

    if provider is None:
        return False, "Provider prov_1 (Dr. Chen) not found in providers"

    if provider.get("sharingDefault") != 3:
        return False, f"Dr. Chen sharingDefault is {provider.get('sharingDefault')}, expected 3"

    return True, "Dr. Chen (prov_1) sharing default changed to 3 successfully"
