import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    templates = state.get("rxTemplates", [])
    tpl_names = [t.get("medicationName", "") for t in templates]
    permanent_rx = state.get("permanentRxMeds", [])
    perm_names = {m.get("medicationName", "") for m in permanent_rx}

    # Templates that should be KEPT (match active permanent Rx)
    should_keep = [
        "Lisinopril 10mg tablet",
        "Metformin 500mg tablet",
        "Atorvastatin 20mg tablet",
        "Omeprazole 20mg capsule",
        "Sertraline 50mg tablet",
        "Amlodipine 5mg tablet",
    ]

    # Templates that should be DELETED (not matching any permanent Rx)
    should_delete = [
        "Lisinopril 20mg tablet",
        "Metformin 1000mg tablet",
        "Atorvastatin 40mg tablet",
        "Amoxicillin 500mg capsule",
        "Azithromycin 250mg tablet (Z-Pack)",
        "Prednisone 10mg tablet (taper)",
    ]

    for name in should_delete:
        if name in tpl_names:
            return False, f"Template '{name}' still exists but patient is not taking it as permanent Rx"

    for name in should_keep:
        if name not in tpl_names:
            return False, f"Template '{name}' was deleted but patient IS taking it as permanent Rx"

    return True, "Template library cleaned: 6 non-current templates deleted, 6 current templates retained"
