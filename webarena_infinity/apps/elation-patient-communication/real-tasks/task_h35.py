import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Clinical Team added to Dr. Kim's Billing Question routing."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Kevin Adebayo (pat_11) wrote about $247 billing charge, assigned to prov_4 (Dr. Kim)
    routing = state.get("messageRouting", {}).get("prov_4", {})
    billing_routing = routing.get("Billing Question", [])

    if "ug_2" not in billing_routing:
        return False, (
            f"Clinical Team (ug_2) not found in Dr. Kim's Billing Question routing. "
            f"Current routing: {billing_routing}"
        )

    return True, "Clinical Team (ug_2) added to Dr. Kim's Billing Question routing"
