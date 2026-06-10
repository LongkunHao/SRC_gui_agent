import requests


def verify(server_url: str) -> tuple[bool, str]:
    """History-based favorites cleanup: remove allergic-reaction antibiotic + other antibiotics."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []
    favs = state.get("settings", {}).get("favoritesDrugIds", [])

    # drug_025 (Amoxicillin — the one that caused the allergic reaction in Nov 2024)
    if "drug_025" in favs:
        errors.append("Amoxicillin (drug_025) is still in favorites — it caused an allergic reaction.")

    # drug_028 (Azithromycin — another antibiotic in favorites)
    if "drug_028" in favs:
        errors.append("Azithromycin (drug_028) is still in favorites — it's an antibiotic that should be removed.")

    if errors:
        return False, " ".join(errors)
    return True, "All antibiotics removed from favorites after medication history review."
