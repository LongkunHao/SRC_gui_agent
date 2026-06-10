import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Torres (prov_2) notification timeframe changed to 'none'."""
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

    timeframe = provider.get("notificationTimeframe")
    if timeframe != "none":
        return False, f"Provider prov_2 notificationTimeframe is '{timeframe}', expected 'none'"

    return True, "Dr. Torres (prov_2) notification timeframe correctly set to 'none'"
