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
    sig_texts = [s.get("text", "") for s in custom_sigs]

    # These capsule sigs should be deleted
    capsule_sigs_to_delete = [
        "Take 1 capsule by mouth once daily",
        "Take 1 capsule by mouth twice daily",
        "Take 1 capsule by mouth three times daily",
        "Take 1 capsule by mouth once daily before breakfast",
    ]

    for sig_text in capsule_sigs_to_delete:
        if sig_text in sig_texts:
            return False, f"Capsule sig '{sig_text}' still present in customSigs, should be deleted"

    # These tablet sigs (oral category) should still be present
    tablet_sigs_to_keep = [
        "Take 1 tablet by mouth once daily",
        "Take 1 tablet by mouth twice daily",
        "Take 1 tablet by mouth three times daily",
    ]

    for sig_text in tablet_sigs_to_keep:
        if sig_text not in sig_texts:
            return False, f"Tablet sig '{sig_text}' missing from customSigs, should be kept"

    # Non-oral sigs should be untouched
    non_oral_sigs = [
        "Apply topically to affected area twice daily",
        "Inhale 1-2 puffs every 4-6 hours as needed",
    ]
    for sig_text in non_oral_sigs:
        if sig_text not in sig_texts:
            return False, f"Non-oral sig '{sig_text}' missing from customSigs, should be untouched"

    return True, "All oral capsule custom sigs deleted, tablet and non-oral sigs retained"
