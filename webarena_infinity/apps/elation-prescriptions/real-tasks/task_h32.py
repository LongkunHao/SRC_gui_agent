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

    # The DAW medication is Losartan 50mg (prx_009)
    # Check old Losartan is discontinued
    losartan_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Losartan 50mg tablet":
            losartan_disc = med
            break
    if losartan_disc is None:
        return False, "Original Losartan 50mg (DAW) not found in discontinuedMeds"

    # Check new Losartan exists in permanentRxMeds without DAW
    losartan_new = None
    for med in permanent_rx:
        if "losartan" in med.get("medicationName", "").lower() and "50mg" in med.get("medicationName", "").lower():
            losartan_new = med
            break
    if losartan_new is None:
        return False, "No new Losartan 50mg found in permanentRxMeds"

    if losartan_new.get("dispenseAsWritten") is True:
        return False, "New Losartan still has dispenseAsWritten=true, should be false (allow generic)"

    qty = losartan_new.get("qty")
    if qty != 30:
        return False, f"New Losartan qty is {qty}, expected 30"

    refills = losartan_new.get("refills", losartan_new.get("refillsRemaining"))
    if refills != 3:
        return False, f"New Losartan refills is {refills}, expected 3"

    # Check pharmacy matches original (Walgreens #7892)
    pharmacy_id = losartan_new.get("pharmacyId", "")
    pharmacy_name = losartan_new.get("pharmacyName", "")
    if pharmacy_id != "pharm_003" and "walgreens" not in pharmacy_name.lower():
        return False, f"New Losartan pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected Walgreens #7892"

    return True, "Original DAW Losartan discontinued, new Losartan prescribed without DAW at Walgreens"
