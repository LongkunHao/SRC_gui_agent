import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Torres's routing for 'General Question' does NOT include Front Desk (ug_1), but still includes prov_2."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    message_routing = state.get("messageRouting", {})

    prov_2_routing = message_routing.get("prov_2")
    if prov_2_routing is None:
        return False, "No message routing found for prov_2 (Dr. Torres)"

    general_question_routing = prov_2_routing.get("General Question")
    if general_question_routing is None:
        return False, "No 'General Question' routing found for prov_2 (Dr. Torres)"

    if "ug_1" in general_question_routing:
        return False, f"'ug_1' (Front Desk) should NOT be in Dr. Torres's 'General Question' routing: {general_question_routing}"

    if "prov_2" not in general_question_routing:
        return False, f"'prov_2' (Dr. Torres) should still be in the 'General Question' routing: {general_question_routing}"

    return True, "Dr. Torres's 'General Question' routing correctly excludes Front Desk (ug_1) and still includes prov_2"
