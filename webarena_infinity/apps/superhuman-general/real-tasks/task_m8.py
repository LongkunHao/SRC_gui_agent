import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check primary timezone is set to Pacific Time
    settings = state.get("settings", {})
    timezone = settings.get("timezone", "")

    pacific_values = [
        "America/Los_Angeles",
        "US/Pacific",
        "Pacific",
        "PT",
        "PST",
        "PDT",
        "Pacific Time",
    ]

    # Check if timezone matches any Pacific-related value (case-insensitive)
    for pv in pacific_values:
        if timezone.lower() == pv.lower():
            return True, f"Primary timezone has been changed to Pacific Time ({timezone})."

    # Also check if it contains "Pacific" or "Los_Angeles"
    if "pacific" in timezone.lower() or "los_angeles" in timezone.lower():
        return True, f"Primary timezone has been changed to Pacific Time ({timezone})."

    return False, f"Primary timezone is '{timezone}', expected a Pacific Time value (e.g., 'America/Los_Angeles')."
