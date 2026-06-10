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
    settings = state.get("settings", {})

    # Amazon Pharmacy = pharm_010
    # New Sertraline at Amazon
    sert_amazon = None
    for med in permanent_rx:
        if med.get("medicationName") == "Sertraline 50mg tablet" and med.get("pharmacyId") == "pharm_010":
            sert_amazon = med
            break

    if sert_amazon is None:
        return False, "Sertraline 50mg tablet not found at Amazon Pharmacy"

    if sert_amazon.get("qty") != 90:
        return False, f"Sertraline qty is {sert_amazon.get('qty')}, expected 90"
    if sert_amazon.get("refills") != 5:
        return False, f"Sertraline refills is {sert_amazon.get('refills')}, expected 5"
    if sert_amazon.get("daysSupply") != 90:
        return False, f"Sertraline daysSupply is {sert_amazon.get('daysSupply')}, expected 90"

    # New Losartan at Amazon
    losar_amazon = None
    for med in permanent_rx:
        if med.get("medicationName") == "Losartan 50mg tablet" and med.get("pharmacyId") == "pharm_010":
            losar_amazon = med
            break

    if losar_amazon is None:
        return False, "Losartan 50mg tablet not found at Amazon Pharmacy"

    if losar_amazon.get("qty") != 90:
        return False, f"Losartan qty is {losar_amazon.get('qty')}, expected 90"
    if losar_amazon.get("refills") != 5:
        return False, f"Losartan refills is {losar_amazon.get('refills')}, expected 5"
    if losar_amazon.get("daysSupply") != 90:
        return False, f"Losartan daysSupply is {losar_amazon.get('daysSupply')}, expected 90"

    # Default pharmacy should be Amazon
    if settings.get("defaultPharmacyId") != "pharm_010":
        return False, f"Default pharmacy is '{settings.get('defaultPharmacyId')}', expected 'pharm_010' (Amazon)"

    return True, "Sertraline and Losartan prescribed at Amazon Pharmacy; default pharmacy updated"
