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
    tpl_names = [t.get("medicationName") for t in templates]

    # Templates that match active permanent Rx (should be KEPT):
    # Lisinopril 10mg, Metformin 500mg, Atorvastatin 20mg, Omeprazole 20mg,
    # Sertraline 50mg, Amlodipine 5mg
    should_keep = [
        "Lisinopril 10mg tablet",
        "Metformin 500mg tablet",
        "Atorvastatin 20mg tablet",
        "Omeprazole 20mg capsule",
        "Sertraline 50mg tablet",
        "Amlodipine 5mg tablet",
    ]

    # Templates whose strength doesn't match (should be DELETED):
    # Lisinopril 20mg (patient takes 10mg), Metformin 1000mg (patient takes 500mg),
    # Atorvastatin 40mg (patient takes 20mg),
    # Amoxicillin 500mg (temporary, not permanent Rx),
    # Azithromycin Z-Pack (not active permanent Rx),
    # Prednisone taper (not active permanent Rx)
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
            return False, f"Template '{name}' still exists but doesn't match any active permanent Rx"

    for name in should_keep:
        if name not in tpl_names:
            return False, f"Template '{name}' was deleted but matches an active permanent Rx"

    return True, "Non-matching strength templates deleted, matching templates retained"
