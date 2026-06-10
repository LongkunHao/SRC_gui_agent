import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the spam email from CryptoGains Now
    target_email = None
    for e in state.get("emails", []):
        if (e.get("subject") == "Make $50K/day with this ONE trick!"
                and e.get("from", {}).get("name") == "CryptoGains Now"):
            target_email = e
            break
    if not target_email:
        return False, "Could not find email 'Make $50K/day with this ONE trick!' from CryptoGains Now."

    # Check that isSpam is False (moved back to inbox)
    if target_email.get("isSpam") == False:
        return True, "CryptoGains spam email has been successfully moved back to inbox (isSpam is False)."
    else:
        return False, f"Email is still marked as spam. isSpam: {target_email.get('isSpam')}"
