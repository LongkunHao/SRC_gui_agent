import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Chen's routing for 'Test Results' includes Clinical Team (ug_2)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    message_routing = state.get("messageRouting", {})

    prov_1_routing = message_routing.get("prov_1")
    if prov_1_routing is None:
        return False, "No message routing found for prov_1 (Dr. Chen)"

    test_results_routing = prov_1_routing.get("Test Results")
    if test_results_routing is None:
        return False, "No 'Test Results' routing found for prov_1 (Dr. Chen)"

    if "ug_2" not in test_results_routing:
        return False, f"'ug_2' (Clinical Team) not in Dr. Chen's 'Test Results' routing: {test_results_routing}"

    return True, "Dr. Chen's 'Test Results' routing correctly includes Clinical Team (ug_2)"
