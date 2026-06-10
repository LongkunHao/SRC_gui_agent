import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # OTC supplements with no prescriber (prescriberName is null):
    # Fish Oil, Calcium+D3, Centrum Silver, Melatonin
    # OTC with prescriber: Vitamin D3 (Dr. Mitchell), Aspirin (Dr. Mitchell)
    no_prescriber_otc = [
        "Fish Oil 1000mg softgel",
        "Calcium 600mg + Vitamin D3 400 IU tablet",
        "Centrum Silver Multivitamin tablet",
        "Melatonin 3mg tablet",
    ]
    prescriber_otc = [
        "Vitamin D3 2000 IU tablet",
        "Aspirin 81mg tablet (low-dose)",
    ]

    permanent_otc = state.get("permanentOtcMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    otc_names = [m.get("medicationName") for m in permanent_otc]

    # No-prescriber OTCs should be discontinued
    for name in no_prescriber_otc:
        if name in otc_names:
            return False, f"{name} still in permanentOtcMeds, should be discontinued"
        disc = any(m.get("medicationName") == name for m in discontinued)
        if not disc:
            return False, f"{name} not found in discontinuedMeds"

    # Prescriber OTCs should remain
    for name in prescriber_otc:
        if name not in otc_names:
            return False, f"{name} removed from permanentOtcMeds but should remain (has prescriber)"

    # Reconciliation should be completed
    patient = state.get("currentPatient", {})
    last_rec = patient.get("lastReconciledDate")
    if not last_rec or last_rec == "2026-01-15T14:30:00Z":
        return False, f"lastReconciledDate not updated (got '{last_rec}')"

    return True, "Med rec completed: 4 non-provider OTC supplements discontinued, 2 provider-documented retained"
