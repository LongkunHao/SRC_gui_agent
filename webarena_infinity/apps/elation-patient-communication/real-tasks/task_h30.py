import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Clinical Team added to all of Dr. Kim's (prov_4) routing categories."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Howard Blackwell (pat_27) has pacemaker + Warfarin, assigned to prov_4 (Dr. Kim)
    categories = [
        "General Question", "Prescription Refill", "Appointment Request",
        "Test Results", "Billing Question", "Referral Request",
        "Medical Records Request", "Other"
    ]

    routing = state.get("messageRouting", {}).get("prov_4", {})

    missing = []
    for cat in categories:
        cat_routing = routing.get(cat, [])
        if "ug_2" not in cat_routing:
            missing.append(f"'{cat}' (current: {cat_routing})")

    if missing:
        return False, (
            f"Clinical Team (ug_2) missing from Dr. Kim's routing for: "
            f"{'; '.join(missing)}"
        )

    return True, "Clinical Team (ug_2) added to all 8 of Dr. Kim's message routing categories"
