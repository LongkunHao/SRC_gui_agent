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

    # Two Walgreens meds: Losartan 50mg (prx_009) and Sertraline 50mg (prx_005)
    for med_name in ["Losartan 50mg tablet", "Sertraline 50mg tablet"]:
        still_active = any(m.get("medicationName") == med_name for m in permanent_rx)
        if still_active:
            return False, f"{med_name} still in permanentRxMeds"
        in_disc = any(m.get("medicationName") == med_name for m in discontinued)
        if not in_disc:
            return False, f"{med_name} not found in discontinuedMeds"
        in_canceled = any(c.get("medicationName") == med_name for c in canceled)
        if not in_canceled:
            return False, f"Cancellation for {med_name} not found in canceledScripts"

    return True, "Both Walgreens medications (Losartan, Sertraline) discontinued with cancellations"
