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

    # Gabapentin 300mg is the most overdue medication (next refill 2026-01-19)
    # A new 90-day prescription should exist at CVS
    new_gaba = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "gabapentin" in name.lower() and "300mg" in name.lower():
            # Look for the new prescription (qty=90, daysSupply=90)
            if med.get("qty") == 90 and med.get("daysSupply") == 90:
                new_gaba = med
                break

    if new_gaba is None:
        return False, "No new Gabapentin 300mg prescription found with qty=90, daysSupply=90"

    if new_gaba.get("pharmacyId") != "pharm_001":
        return False, f"New Gabapentin pharmacy is '{new_gaba.get('pharmacyName')}', expected CVS #4521"
    if new_gaba.get("refills") != 5:
        return False, f"New Gabapentin refills is {new_gaba.get('refills')}, expected 5"

    sig = new_gaba.get("sig", "").lower()
    if "three times" not in sig and "tid" not in sig and "3 times" not in sig:
        return False, f"New Gabapentin sig should match original TID dosing, got: '{new_gaba.get('sig')}'"

    return True, "New 90-day Gabapentin prescription created at CVS #4521"
