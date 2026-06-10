import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})
    errors = []

    # Check default pharmacy
    if settings.get("defaultPharmacy") != "pharm_009":
        errors.append(f"Expected defaultPharmacy 'pharm_009' (Capsule Pharmacy SF), got '{settings.get('defaultPharmacy')}'.")

    # Check default days supply
    if settings.get("defaultDaysSupply") != 90:
        errors.append(f"Expected defaultDaysSupply 90, got {settings.get('defaultDaysSupply')}.")

    # Check default refills
    if settings.get("defaultRefills") != 3:
        errors.append(f"Expected defaultRefills 3, got {settings.get('defaultRefills')}.")

    # Check signature requirement disabled
    if settings.get("signatureRequired") is not False:
        errors.append(f"Expected signatureRequired False, got {settings.get('signatureRequired')}.")

    # Check print format
    if settings.get("printFormat") != "compact":
        errors.append(f"Expected printFormat 'compact', got '{settings.get('printFormat')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Settings updated correctly: Capsule Pharmacy SF, 90 days supply, 3 refills, no signature, compact print."
