import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    rx_templates = state.get("rxTemplates", [])

    # Omeprazole template should have updated sig and refills
    omeprazole_tpl = None
    for tpl in rx_templates:
        if tpl.get("medicationName") == "Omeprazole 20mg capsule":
            omeprazole_tpl = tpl
            break

    if omeprazole_tpl is None:
        return False, "Omeprazole 20mg capsule template not found"

    sig = omeprazole_tpl.get("sig", "").lower()
    if "twice daily" not in sig and "bid" not in sig:
        return False, f"Omeprazole template sig should include 'twice daily', got: '{omeprazole_tpl.get('sig')}'"
    if "before meals" not in sig:
        return False, f"Omeprazole template sig should include 'before meals', got: '{omeprazole_tpl.get('sig')}'"

    if omeprazole_tpl.get("refills") != 5:
        return False, f"Omeprazole template refills is {omeprazole_tpl.get('refills')}, expected 5"

    # Sertraline template should be deleted
    sertraline_tpl = any(
        tpl.get("medicationName") == "Sertraline 50mg tablet" for tpl in rx_templates
    )
    if sertraline_tpl:
        return False, "Sertraline 50mg tablet template should be deleted"

    return True, "Omeprazole template updated (BID before meals, 5 refills); Sertraline template deleted"
