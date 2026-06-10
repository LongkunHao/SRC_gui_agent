# Task: Re-invite expired Stripe delegate — remove expired entry and re-add.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    delegates = state.get("delegates", [])

    # Jake Morrison (jake.morrison@gmail.com) had an expired delegate entry
    # After re-invitation, there should be exactly one entry with pending status
    jake_delegates = [d for d in delegates if d.get("email") == "jake.morrison@gmail.com"]

    if len(jake_delegates) == 0:
        errors.append(
            "No delegate found for jake.morrison@gmail.com (should be re-invited)"
        )
    elif len(jake_delegates) > 1:
        errors.append(
            f"Found {len(jake_delegates)} delegate entries for jake.morrison@gmail.com "
            "(expected exactly 1)"
        )
    else:
        d = jake_delegates[0]
        if d.get("status") == "expired":
            errors.append(
                "Jake Morrison's delegate status is still 'expired' "
                "(should be 'pending' after re-invitation)"
            )

    # No expired delegate should remain
    expired = [d for d in delegates if d.get("status") == "expired"]
    if expired:
        expired_emails = [d.get("email") for d in expired]
        errors.append(f"Expired delegates still exist: {expired_emails}")

    if errors:
        return False, "; ".join(errors)
    return True, "Jake Morrison's expired delegate removed and re-invited as pending."
