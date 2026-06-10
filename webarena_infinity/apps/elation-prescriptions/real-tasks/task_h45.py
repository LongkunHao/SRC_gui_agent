import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    custom_sigs = state.get("customSigs", [])

    # Original PRN sigs that should be deleted:
    old_prn_sigs = [
        "Take 1 tablet by mouth every 4-6 hours as needed for pain",
        "Take 1 tablet by mouth every 6 hours as needed for pain",
        "Take 1 tablet by mouth every 8 hours as needed",
        "Take 1 tablet by mouth once daily as needed",
    ]

    for sig_text in old_prn_sigs:
        found = any(s.get("text") == sig_text for s in custom_sigs)
        if found:
            return False, f"PRN sig '{sig_text}' still exists, should have been deleted"

    # New PRN sig should exist
    new_sig = "Take 1 tablet by mouth every 4-6 hours as needed for nausea"
    found_new = any(
        s.get("text") == new_sig and s.get("category") == "prn"
        for s in custom_sigs
    )
    if not found_new:
        return False, f"New PRN sig '{new_sig}' not found in customSigs"

    return True, "All old PRN sigs deleted, new nausea PRN sig added"
