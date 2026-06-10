import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Offline collaborators in seed data: James O'Brien (user_004),
    # Priya Sharma (user_005), Elena Kowalski (user_007)
    offline_user_ids = {"user_004", "user_005", "user_007"}

    # All comments from offline collaborators should be resolved
    for c in state.get("comments", []):
        user_id = c.get("userId", "")
        if user_id in offline_user_ids:
            if c.get("resolved") is not True:
                author = c.get("userName", user_id)
                errors.append(f"Comment by offline collaborator '{author}' is not resolved")

    # Check Warm Sunset renamed to Coral Reef
    found_coral = False
    for ts in state.get("templateStyles", []):
        if ts.get("id") == "ts_003":
            name = ts.get("name")
            if name == "Coral Reef":
                found_coral = True
            else:
                errors.append(f"Template ts_003 name is '{name}', expected 'Coral Reef'")
            break

    if not found_coral and not any("ts_003" in e for e in errors):
        errors.append("Template style ts_003 not found")

    if errors:
        return False, "; ".join(errors)
    return True, "Offline collaborators' comments resolved; Warm Sunset renamed to Coral Reef"
