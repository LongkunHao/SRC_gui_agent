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
    discontinued = state.get("discontinuedMeds", [])
    canceled = state.get("canceledScripts", [])

    # Losartan is the ARB — check it's NOT in permanentRxMeds
    for med in permanent_rx:
        if med.get("medicationName") == "Losartan 50mg tablet":
            return False, "Losartan 50mg tablet still in permanentRxMeds"

    # Check Losartan IS in discontinuedMeds
    losartan_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Losartan 50mg tablet":
            losartan_disc = med
            break
    if losartan_disc is None:
        return False, "Losartan 50mg tablet not found in discontinuedMeds"

    # Check cancellation was sent to pharmacy
    losartan_cancel = None
    for script in canceled:
        if "losartan" in script.get("medicationName", "").lower():
            losartan_cancel = script
            break
    if losartan_cancel is None:
        return False, "No cancellation found for Losartan in canceledScripts"

    # Verify Lisinopril (ACE inhibitor) is still active
    lisinopril = None
    for med in permanent_rx:
        if med.get("medicationName") == "Lisinopril 10mg tablet":
            lisinopril = med
            break
    if lisinopril is None:
        return False, "Lisinopril 10mg tablet missing from permanentRxMeds — should still be active"

    return True, "Losartan (ARB) discontinued with cancellation, Lisinopril (ACE) retained"
