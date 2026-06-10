import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    splits = state.get("splits", [])
    split_names = [s.get("name", "") for s in splits]

    errors = []
    if "Feeds" in split_names:
        errors.append("Split 'Feeds' still exists (should be deleted).")
    if "Notifications" in split_names:
        errors.append("Split 'Notifications' still exists (should be deleted).")

    if errors:
        return False, " | ".join(errors)

    return True, "Custom splits 'Feeds' and 'Notifications' have been deleted."
