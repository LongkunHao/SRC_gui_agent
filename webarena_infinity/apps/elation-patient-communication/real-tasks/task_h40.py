import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify providers with 24-hour notification now have 1 week."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Providers who had 24_hours: prov_2 (Dr. Torres), prov_5 (Amanda Wright)
    target_providers = {"prov_2", "prov_5"}

    wrong = []
    for prov in state.get("providers", []):
        if prov.get("id") in target_providers:
            tf = prov.get("notificationTimeframe")
            if tf != "1_week":
                name = f"{prov.get('firstName', '')} {prov.get('lastName', '')}"
                wrong.append(f"{name} (timeframe: {tf})")

    if wrong:
        return False, (
            f"Providers still not set to 1 week: {', '.join(wrong)}"
        )

    # Verify other providers unchanged
    unchanged = {
        "prov_1": "48_hours",
        "prov_3": "72_hours",
        "prov_4": "48_hours",
    }
    for prov in state.get("providers", []):
        pid = prov.get("id")
        if pid in unchanged:
            expected = unchanged[pid]
            actual = prov.get("notificationTimeframe")
            if actual != expected:
                name = f"{prov.get('firstName', '')} {prov.get('lastName', '')}"
                return False, (
                    f"{name}'s notification timeframe changed to '{actual}' "
                    f"but should have remained '{expected}'"
                )

    return True, "Dr. Torres and Amanda Wright notification timeframes changed to 1 week"
