import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Kim (prov_4) virtual visit instructions updated with new Zoom link."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    providers = state.get("providers", [])

    provider = None
    for p in providers:
        if p.get("id") == "prov_4":
            provider = p
            break

    if provider is None:
        return False, "Provider prov_4 (Dr. Kim) not found in providers"

    instructions = provider.get("virtualVisitInstructions", "")
    if "https://zoom.us/j/9999999999" not in instructions:
        return False, f"prov_4 virtualVisitInstructions does not contain 'https://zoom.us/j/9999999999': '{instructions}'"

    return True, "Dr. Kim (prov_4) virtual visit instructions correctly updated with new Zoom link"
