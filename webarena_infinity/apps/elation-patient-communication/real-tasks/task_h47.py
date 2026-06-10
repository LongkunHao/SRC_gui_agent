import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that Tyler Robinson (pat_39) had their Passport invitation resent (invitedAt changed
    from seed value) and 'Telehealth Preferred' was added to their tags."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    patients = state.get("patients", [])
    if not patients:
        return False, "No patients found in state"

    pat_39 = None
    for p in patients:
        if p.get("id") == "pat_39":
            pat_39 = p
            break

    if not pat_39:
        return False, "Patient pat_39 (Tyler Robinson) not found"

    errors = []

    # Check invitedAt changed from seed value
    seed_invited_at = "2026-01-20T14:00:00Z"
    invited_at = pat_39.get("invitedAt", "")
    if invited_at == seed_invited_at:
        errors.append(
            f"invitedAt is still the seed value '{seed_invited_at}', expected it to be updated (resent)"
        )
    if not invited_at:
        errors.append("invitedAt is empty or missing")

    # Check 'Telehealth Preferred' in tags
    tags = pat_39.get("tags", [])
    if "Telehealth Preferred" not in tags:
        errors.append(f"'Telehealth Preferred' not found in pat_39 tags. Current tags: {tags}")

    if errors:
        return False, "; ".join(errors)

    return True, (
        f"pat_39 invitation resent (invitedAt changed to '{invited_at}') and "
        f"'Telehealth Preferred' added to tags"
    )
