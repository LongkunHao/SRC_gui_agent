import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The SSRI is Sertraline 50mg tablet, currently at Walgreens #7892
    # Task: prescribe a refill of the same med at CVS #4521
    permanent_rx = state.get("permanentRxMeds", [])

    # Find new Sertraline at CVS
    sertraline_at_cvs = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "sertraline" in name.lower() and "50mg" in name.lower():
            if med.get("pharmacyId") == "pharm_001" or "cvs" in med.get("pharmacyName", "").lower():
                sertraline_at_cvs = med
                break

    if sertraline_at_cvs is None:
        return False, "No Sertraline 50mg prescription at CVS #4521 found"

    # Check qty, refills, days supply
    if sertraline_at_cvs.get("qty") != 30:
        return False, f"Qty is {sertraline_at_cvs.get('qty')}, expected 30"

    refills = sertraline_at_cvs.get("refills", sertraline_at_cvs.get("refillsRemaining"))
    if refills != 5:
        return False, f"Refills is {refills}, expected 5"

    if sertraline_at_cvs.get("daysSupply") != 30:
        return False, f"Days supply is {sertraline_at_cvs.get('daysSupply')}, expected 30"

    # Sig should match original
    sig = sertraline_at_cvs.get("sig", "")
    if "once daily" not in sig.lower() or "morning" not in sig.lower():
        return False, f"Sig doesn't match original morning dosing: '{sig}'"

    return True, "Sertraline 50mg refill prescribed at CVS #4521 with correct parameters"
