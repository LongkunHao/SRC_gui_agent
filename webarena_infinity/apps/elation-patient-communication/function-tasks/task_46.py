import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Kim's routing for 'Prescription Refill' includes Nurses group (ug_3)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    message_routing = state.get("messageRouting", {})

    prov_4_routing = message_routing.get("prov_4")
    if prov_4_routing is None:
        return False, "No message routing found for prov_4 (Dr. Kim)"

    refill_routing = prov_4_routing.get("Prescription Refill")
    if refill_routing is None:
        return False, "No 'Prescription Refill' routing found for prov_4 (Dr. Kim)"

    if "ug_3" not in refill_routing:
        return False, f"'ug_3' (Nurses) not in Dr. Kim's 'Prescription Refill' routing: {refill_routing}"

    return True, "Dr. Kim's 'Prescription Refill' routing correctly includes Nurses group (ug_3)"
