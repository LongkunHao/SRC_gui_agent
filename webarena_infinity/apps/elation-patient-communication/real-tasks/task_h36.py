import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify all unread inbox messages marked as read and Chen notification set to none."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # All from_patient unread letters in seed:
    # ltr_4, ltr_6, ltr_10, ltr_15, ltr_19, ltr_20, ltr_23, ltr_24, ltr_29, ltr_39, ltr_46, ltr_47
    unread_ids = {
        "ltr_4", "ltr_6", "ltr_10", "ltr_15", "ltr_19", "ltr_20",
        "ltr_23", "ltr_24", "ltr_29", "ltr_39", "ltr_46", "ltr_47"
    }

    still_unread = []
    for ltr in state.get("patientLetters", []):
        if ltr.get("id") in unread_ids and not ltr.get("isRead"):
            still_unread.append(ltr.get("id"))

    if still_unread:
        return False, (
            f"Messages still unread: {', '.join(sorted(still_unread))}"
        )

    # Check Dr. Chen's notification timeframe
    for prov in state.get("providers", []):
        if prov.get("id") == "prov_1":
            if prov.get("notificationTimeframe") != "none":
                return False, (
                    f"Dr. Chen's notification timeframe is "
                    f"'{prov.get('notificationTimeframe')}', expected 'none'"
                )
            break

    return True, "All 12 unread inbox messages marked as read and Dr. Chen's notification set to none"
