import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Front Desk replaced by Clinical Team in Okafor's routing."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    routing = state.get("messageRouting", {}).get("prov_3", {})

    # Categories where Front Desk (ug_1) was originally present:
    # Appointment Request, Billing Question, Medical Records Request
    swap_categories = ["Appointment Request", "Billing Question", "Medical Records Request"]

    errors = []
    for cat in swap_categories:
        cat_routing = routing.get(cat, [])
        if "ug_1" in cat_routing:
            errors.append(f"'{cat}' still contains Front Desk (ug_1)")
        if "ug_2" not in cat_routing:
            errors.append(f"'{cat}' missing Clinical Team (ug_2)")

    if errors:
        return False, "; ".join(errors)

    # Also verify ug_1 is not in ANY category for prov_3
    for cat, recipients in routing.items():
        if "ug_1" in recipients:
            return False, f"Front Desk (ug_1) still found in '{cat}' routing"

    return True, "Front Desk replaced by Clinical Team in all applicable Okafor routing categories"
