import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The medication prescribed by Dr. Michael Chen is Losartan 50mg,
    # dispensed at Walgreens #7892 (pharm_003)
    settings = state.get("settings", {})
    default_pharmacy = settings.get("defaultPharmacyId")

    if default_pharmacy != "pharm_003":
        return False, (
            f"Default pharmacy is '{default_pharmacy}', expected 'pharm_003' "
            f"(Walgreens #7892 — the pharmacy for Dr. Chen's prescription)"
        )

    return True, "Default pharmacy changed to Walgreens #7892 (Dr. Chen's Losartan pharmacy)"
