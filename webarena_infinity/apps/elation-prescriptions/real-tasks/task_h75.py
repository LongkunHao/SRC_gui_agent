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

    # Centrum Silver should be discontinued
    centrum_active = any(
        "centrum" in m.get("medicationName", "").lower() for m in permanent_otc
    )
    if centrum_active:
        return False, "Centrum Silver Multivitamin still active — should be discontinued"

    centrum_disc = any(
        "centrum" in m.get("medicationName", "").lower() for m in discontinued
    )
    if not centrum_disc:
        return False, "Centrum Silver Multivitamin not found in discontinuedMeds"

    # Probiotic should be documented as OTC
    probiotic = None
    for med in permanent_otc:
        if "probiotic" in med.get("medicationName", "").lower():
            probiotic = med
            break

    if probiotic is None:
        return False, "Probiotic not found in permanentOtcMeds"

    sig = probiotic.get("sig", "").lower()
    if "once daily" not in sig and "daily" not in sig:
        return False, f"Probiotic sig should include daily dosing, got: '{probiotic.get('sig')}'"

    return True, "Centrum Silver discontinued; Probiotic documented as OTC supplement"
