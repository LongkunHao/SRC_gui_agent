import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Remove Anika Patel from all presentations except ones she created."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    anika_id = "user_003"
    # Presentations she was in sharedWith but did NOT create:
    # pres_001, pres_002, pres_006, pres_007, pres_008, pres_013, pres_014, pres_016
    should_be_removed_from = {
        "pres_001", "pres_002", "pres_006", "pres_007",
        "pres_008", "pres_013", "pres_014", "pres_016"
    }

    errors = []

    for p in presentations:
        pid = p.get("id")
        shared = set(p.get("shareSettings", {}).get("sharedWith", []))

        if pid in should_be_removed_from and anika_id in shared:
            errors.append(
                f"{pid} ({p.get('title')}): Anika (user_003) should be removed "
                f"but is still in sharedWith"
            )

    if errors:
        return False, "; ".join(errors)

    return True, "Anika Patel removed from 8 presentations she didn't create."
