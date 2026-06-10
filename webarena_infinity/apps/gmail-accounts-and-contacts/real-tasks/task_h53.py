# Task: Merge CloudNine duplicates, remove CloudNine delegates.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    delegates = state.get("delegates", [])
    merges = state.get("mergeSuggestions", [])

    # CloudNine merge (merge_1) should be dismissed
    merge1 = None
    for m in merges:
        if m.get("id") == "merge_1":
            merge1 = m
            break
    if merge1 is None:
        errors.append("merge_1 not found")
    elif not merge1.get("dismissed"):
        errors.append("CloudNine merge suggestion (merge_1) should be dismissed")

    # Raj Kapoor (secondary) should be removed after merge
    raj_exists = any(
        c.get("firstName") == "Raj" and c.get("lastName") == "Kapoor"
        for c in contacts
    )
    if raj_exists:
        errors.append("Raj Kapoor should be merged into Priya Sharma (deleted)")

    # Priya Sharma (primary) should still exist with merged data
    priya = None
    for c in contacts:
        if c.get("firstName") == "Priya" and c.get("lastName") == "Sharma":
            priya = c
            break
    if priya is None:
        errors.append("Priya Sharma (merge primary) not found")

    # No CloudNine delegate should remain
    for d in delegates:
        if d.get("email", "").endswith("@cloudnine.dev"):
            errors.append(
                f"Delegate '{d.get('email')}' should be removed (cloudnine.dev domain)"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "CloudNine contacts merged, CloudNine delegates removed."
