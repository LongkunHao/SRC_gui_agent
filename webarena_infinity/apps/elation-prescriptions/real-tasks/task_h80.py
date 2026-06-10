import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    permanent_rx = state.get("permanentRxMeds", [])
    temporary = state.get("temporaryMeds", [])
    discontinued = state.get("discontinuedMeds", [])

    # Prednisone should be discontinued
    pred_active = any(
        m.get("medicationName") == "Prednisone 10mg tablet" for m in temporary
    )
    if pred_active:
        return False, "Prednisone 10mg tablet still in temporaryMeds — should be discontinued"

    pred_disc = any(
        m.get("medicationName") == "Prednisone 10mg tablet" for m in discontinued
    )
    if not pred_disc:
        return False, "Prednisone 10mg tablet not found in discontinuedMeds"

    # Amoxicillin should be discontinued
    amox_active = any(
        m.get("medicationName") == "Amoxicillin 500mg capsule" for m in temporary
    )
    if amox_active:
        return False, "Amoxicillin 500mg capsule still in temporaryMeds — should be discontinued"

    amox_disc = any(
        m.get("medicationName") == "Amoxicillin 500mg capsule" for m in discontinued
    )
    if not amox_disc:
        return False, "Amoxicillin 500mg capsule not found in discontinuedMeds"

    rx_templates = state.get("rxTemplates", [])

    # Prednisone taper template should be deleted
    pred_tpl = any(
        "prednisone" in tpl.get("medicationName", "").lower() for tpl in rx_templates
    )
    if pred_tpl:
        return False, "Prednisone template should be deleted"

    # Amoxicillin template should be deleted
    amox_tpl = any(
        tpl.get("medicationName") == "Amoxicillin 500mg capsule" for tpl in rx_templates
    )
    if amox_tpl:
        return False, "Amoxicillin 500mg capsule template should be deleted"

    return True, "Prednisone and Amoxicillin discontinued; their Rx templates deleted"
