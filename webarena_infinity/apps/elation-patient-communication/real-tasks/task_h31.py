import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify all Geriatric + opted_in patients are now opted out of SMS."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Geriatric patients who were opted_in in seed data:
    # pat_10 (Helen Matsumoto), pat_19 (Frank DeLuca), pat_36 (Martha Reeves-Whitfield),
    # pat_43 (Philip Tran), pat_50 (Deborah Takahashi)
    expected_opted_out = {"pat_10", "pat_19", "pat_36", "pat_43", "pat_50"}

    still_opted_in = []
    for pat in state.get("patients", []):
        if pat.get("id") in expected_opted_out:
            if pat.get("smsOptInStatus") != "opted_out":
                name = f"{pat.get('firstName', '')} {pat.get('lastName', '')}"
                still_opted_in.append(
                    f"{name} (status: {pat.get('smsOptInStatus')})"
                )

    if still_opted_in:
        return False, (
            f"Geriatric patients still not opted out of SMS: "
            f"{', '.join(still_opted_in)}"
        )

    return True, "All 5 Geriatric patients who were opted in are now opted out of SMS"
