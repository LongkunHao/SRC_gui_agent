import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Jessica Okafor (prov_3) virtual visit activated with Zoom instructions."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    providers = state.get("providers", [])

    provider = None
    for p in providers:
        if p.get("id") == "prov_3":
            provider = p
            break

    if provider is None:
        return False, "Provider prov_3 (Jessica Okafor) not found in providers"

    if provider.get("virtualVisitActivated") is not True:
        return False, f"prov_3 virtualVisitActivated is {provider.get('virtualVisitActivated')}, expected True"

    instructions = provider.get("virtualVisitInstructions", "")
    if "https://zoom.us/j/1234567890" not in instructions:
        return False, f"prov_3 virtualVisitInstructions does not contain 'https://zoom.us/j/1234567890': '{instructions}'"

    return True, "Jessica Okafor (prov_3) virtual visit correctly activated with Zoom link"
