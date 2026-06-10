import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    require_allergy_review = settings.get("requireAllergyReview")

    if require_allergy_review is not False:
        return False, f"Expected settings.requireAllergyReview to be False, but got {require_allergy_review}."

    return True, "Allergy review requirement has been turned off."
