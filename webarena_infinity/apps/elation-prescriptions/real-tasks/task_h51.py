import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Known major drug-drug interaction between active permanent Rx meds:
    # Lisinopril (ACE inhibitor) + Losartan (ARB) — di_001, severity: major
    # Lisinopril startDate: 2019-04-01
    # Losartan startDate: 2025-06-15 ← more recent, should be discontinued
    permanent_rx = state.get("permanentRxMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    canceled = state.get("canceledScripts", [])

    losartan_active = any(m.get("medicationName") == "Losartan 50mg tablet" for m in permanent_rx)
    if losartan_active:
        return False, "Losartan 50mg tablet still active — it was started more recently and should be discontinued"

    losartan_disc = any(m.get("medicationName") == "Losartan 50mg tablet" for m in discontinued)
    if not losartan_disc:
        return False, "Losartan 50mg tablet not found in discontinuedMeds"

    losartan_canceled = any(c.get("medicationName") == "Losartan 50mg tablet" for c in canceled)
    if not losartan_canceled:
        return False, "Cancellation for Losartan not sent to pharmacy"

    # Lisinopril should still be active
    lisinopril_active = any(m.get("medicationName") == "Lisinopril 10mg tablet" for m in permanent_rx)
    if not lisinopril_active:
        return False, "Lisinopril 10mg tablet was removed but should remain (started earlier)"

    return True, "Losartan (more recent) discontinued with cancellation; Lisinopril (older) retained"
