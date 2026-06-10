import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check signature has been updated
    settings = state.get("settings", {})
    signature = settings.get("signature", "")

    if "Chief Product Officer" not in signature:
        return False, f"Signature does not contain 'Chief Product Officer'. Current signature: {signature}"

    if "VP of Product" in signature:
        return False, f"Signature still contains 'VP of Product'. Current signature: {signature}"

    return True, "Signature has been updated to say 'Chief Product Officer' instead of 'VP of Product'."
