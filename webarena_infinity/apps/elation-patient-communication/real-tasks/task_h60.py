import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify providers with 48-hour notification (prov_1, prov_4) added to
    Dr. Torres's (prov_2) Referral Request routing, and others not added."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    routing = state.get("messageRouting", {}).get("prov_2", {})
    referral_routing = routing.get("Referral Request", [])

    # Providers with 48_hours: prov_1 (Dr. Chen), prov_4 (Dr. Kim)
    expected_present = {
        "prov_1": "Dr. Chen",
        "prov_4": "Dr. Kim"
    }

    missing = []
    for pid, name in expected_present.items():
        if pid not in referral_routing:
            missing.append(f"{name} ({pid})")

    if missing:
        return False, (
            f"48-hour providers missing from Dr. Torres's Referral Request routing: "
            f"{', '.join(missing)}. Current routing: {referral_routing}"
        )

    # Verify providers that should NOT be added (not 48_hours)
    should_not_be_present = {
        "prov_3": ("Jessica Okafor", "72_hours"),
        "prov_5": ("Amanda Wright", "24_hours")
    }

    incorrectly_added = []
    for pid, (name, timeframe) in should_not_be_present.items():
        if pid in referral_routing:
            incorrectly_added.append(f"{name} ({pid}, {timeframe})")

    if incorrectly_added:
        return False, (
            f"Non-48-hour providers incorrectly added to Dr. Torres's "
            f"Referral Request routing: {', '.join(incorrectly_added)}"
        )

    return True, (
        "Dr. Chen (prov_1) and Dr. Kim (prov_4) added to Dr. Torres's "
        "Referral Request routing; non-48-hour providers correctly excluded"
    )
