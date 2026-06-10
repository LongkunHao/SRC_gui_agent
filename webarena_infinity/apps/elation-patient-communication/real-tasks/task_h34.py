import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify PA notification changed to 1 week and added to Chen's Referral Request routing."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Find the physician assistant (prov_5, Amanda Wright)
    pa = None
    for prov in state.get("providers", []):
        if prov.get("role") == "physician_assistant":
            pa = prov
            break

    if pa is None:
        return False, "No physician assistant found in providers"

    if pa.get("notificationTimeframe") != "1_week":
        return False, (
            f"PA's notification timeframe is '{pa.get('notificationTimeframe')}', "
            f"expected '1_week'"
        )

    # Check PA is in Dr. Chen's Referral Request routing
    routing = state.get("messageRouting", {}).get("prov_1", {})
    referral_routing = routing.get("Referral Request", [])
    if pa.get("id") not in referral_routing:
        return False, (
            f"PA ({pa.get('id')}) not found in Dr. Chen's Referral Request routing. "
            f"Current routing: {referral_routing}"
        )

    return True, (
        f"PA {pa.get('firstName')} {pa.get('lastName')} notification set to 1 week "
        f"and added to Dr. Chen's Referral Request routing"
    )
