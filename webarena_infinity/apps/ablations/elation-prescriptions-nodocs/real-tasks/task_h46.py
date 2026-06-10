import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Robert's HF regimen: beta blocker on hold, aldosterone antagonist 50mg, SGLT2 discontinued."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_028 Carvedilol (beta blocker) -> on-hold
    rx_028 = next((r for r in state["prescriptions"] if r["id"] == "rx_028"), None)
    if not rx_028:
        errors.append("Prescription rx_028 (Carvedilol) not found.")
    elif rx_028.get("status") != "on-hold":
        errors.append(f"Expected rx_028 (Carvedilol/beta blocker) status 'on-hold', got '{rx_028.get('status')}'.")

    # rx_029 Spironolactone (aldosterone antagonist) -> dosage 50mg
    rx_029 = next((r for r in state["prescriptions"] if r["id"] == "rx_029"), None)
    if not rx_029:
        errors.append("Prescription rx_029 (Spironolactone) not found.")
    elif "50" not in str(rx_029.get("dosage", "")):
        errors.append(f"Expected rx_029 (Spironolactone/aldosterone antagonist) dosage containing '50', got '{rx_029.get('dosage')}'.")

    # rx_027 Empagliflozin (SGLT2 inhibitor) -> discontinued
    rx_027 = next((r for r in state["prescriptions"] if r["id"] == "rx_027"), None)
    if not rx_027:
        errors.append("Prescription rx_027 (Empagliflozin) not found.")
    elif rx_027.get("status") != "discontinued":
        errors.append(f"Expected rx_027 (Empagliflozin/SGLT2) status 'discontinued', got '{rx_027.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Robert's heart failure regimen adjusted correctly by drug class."
