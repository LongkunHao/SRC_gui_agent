import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Pacific Heights Office location added, CPT code 99215 added,
    and Dr. Kim's sharing default set to 3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    practice_settings = state.get("practiceSettings", {})

    # Check Pacific Heights Office location
    locations = practice_settings.get("practiceLocations", [])
    ph_found = False
    for loc in locations:
        if loc.get("name") == "Pacific Heights Office":
            ph_found = True
            address = loc.get("address", "")
            if "3500 California Street" not in address:
                return False, (
                    f"Pacific Heights Office has wrong address: '{address}'. "
                    f"Expected '3500 California Street, San Francisco, CA 94118'"
                )
            pos_code = loc.get("posCode")
            if str(pos_code) != "11":
                return False, (
                    f"Pacific Heights Office has POS code '{pos_code}', expected '11'"
                )
            break

    if not ph_found:
        location_names = [loc.get("name") for loc in locations]
        return False, (
            f"Pacific Heights Office not found in practice locations. "
            f"Current locations: {location_names}"
        )

    # Check CPT code 99215
    cpt_codes = practice_settings.get("cptCodes", [])
    code_values = [str(c.get("code", "")) for c in cpt_codes]

    if "99215" not in code_values:
        return False, (
            f"CPT code '99215' not found in billing codes. "
            f"Current codes: {code_values}"
        )

    # Check Dr. Kim (prov_4) sharing default
    for prov in state.get("providers", []):
        if prov.get("id") == "prov_4":
            sharing_default = prov.get("sharingDefault")
            if sharing_default != 3:
                return False, (
                    f"Dr. Kim's sharingDefault is {sharing_default}, expected 3"
                )
            break

    return True, (
        "Pacific Heights Office added, CPT code 99215 added, "
        "and Dr. Kim's sharing default set to 3"
    )
