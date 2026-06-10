import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    permanent_otc = state.get("permanentOtcMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    patient = state.get("currentPatient", {})

    # Calcium+D3 combo should be discontinued (redundant vitamin D)
    calcium_d3_active = any(
        "calcium" in m.get("medicationName", "").lower() and
        "vitamin d" in m.get("medicationName", "").lower()
        for m in permanent_otc
    )
    if calcium_d3_active:
        return False, "Calcium+Vitamin D3 combination still active, should be discontinued"

    calcium_d3_disc = any(
        "calcium" in m.get("medicationName", "").lower() and
        "vitamin d" in m.get("medicationName", "").lower()
        for m in discontinued
    )
    if not calcium_d3_disc:
        return False, "Calcium+Vitamin D3 combination not found in discontinuedMeds"

    # Standalone Vitamin D3 should still be active
    vit_d3_active = any(
        m.get("medicationName") == "Vitamin D3 2000 IU tablet" for m in permanent_otc
    )
    if not vit_d3_active:
        return False, "Standalone Vitamin D3 2000 IU was removed but should remain"

    # Reconciliation should be completed
    last_rec = patient.get("lastReconciledDate", "")
    if last_rec == "2026-01-15T14:30:00Z" or not last_rec:
        return False, f"lastReconciledDate not updated (still '{last_rec}')"

    return True, "Calcium+D3 combo discontinued during med rec; standalone D3 retained"
