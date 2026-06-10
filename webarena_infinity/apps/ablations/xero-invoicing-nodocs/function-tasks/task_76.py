import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    con = next((c for c in state["contacts"] if c["name"] == "Harmony Music Academy"), None)
    if not con:
        return False, "Contact 'Harmony Music Academy' not found."
    addr = con.get("billingAddress", {})
    if addr.get("street") != "120 Willis Street":
        return False, f"Expected street '120 Willis Street', got '{addr.get('street')}'"
    if addr.get("city") != "Wellington":
        return False, f"Expected city 'Wellington', got '{addr.get('city')}'"
    if addr.get("region") != "Wellington":
        return False, f"Expected region 'Wellington', got '{addr.get('region')}'"
    if addr.get("postalCode") != "6011":
        return False, f"Expected postal code '6011', got '{addr.get('postalCode')}'"
    if addr.get("country") != "New Zealand":
        return False, f"Expected country 'New Zealand', got '{addr.get('country')}'"
    return True, "Billing address of Harmony Music Academy updated correctly."
