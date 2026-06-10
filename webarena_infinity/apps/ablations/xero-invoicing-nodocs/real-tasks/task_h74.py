"""Verify: All Wellington contacts have billing postal code updated to 6140."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    contacts = state.get("contacts", [])
    errors = []

    # Wellington contacts: Nexus Technologies (con_4), Harmony Music (con_13), Apex Legal (con_18)
    wellington_contacts = [
        ("con_4", "Nexus Technologies Ltd"),
        ("con_13", "Harmony Music Academy"),
        ("con_18", "Apex Legal Partners"),
    ]
    for con_id, con_name in wellington_contacts:
        con = next((c for c in contacts if c["id"] == con_id), None)
        if not con:
            errors.append(f"{con_name} ({con_id}) not found")
            continue
        postal = con.get("billingAddress", {}).get("postalCode")
        if postal != "6140":
            errors.append(f"{con_name} postalCode is '{postal}', expected '6140'")

    if errors:
        return False, "; ".join(errors)
    return True, "All Wellington contacts updated to postal code 6140"
