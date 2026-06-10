import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify William Chang (pat_13) email updated and Passport invitation resent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    pat_13 = None
    for pat in state.get("patients", []):
        if pat.get("id") == "pat_13":
            pat_13 = pat
            break

    if pat_13 is None:
        return False, "Patient pat_13 (William Chang) not found"

    # Check email updated
    email = pat_13.get("email")
    if email != "william.chang.new@gmail.com":
        return False, (
            f"William Chang's email is '{email}', "
            f"expected 'william.chang.new@gmail.com'"
        )

    # Check invitation resent (invitedAt should differ from seed value)
    seed_invited_at = "2026-02-01T09:00:00Z"
    invited_at = pat_13.get("invitedAt")

    if invited_at is None:
        return False, "William Chang's invitedAt is None — invitation not resent"

    if invited_at == seed_invited_at:
        return False, (
            f"William Chang's invitedAt is still '{seed_invited_at}' — "
            f"invitation was not resent (timestamp unchanged)"
        )

    return True, (
        f"William Chang's email updated to 'william.chang.new@gmail.com' "
        f"and Passport invitation resent (invitedAt: {invited_at})"
    )
