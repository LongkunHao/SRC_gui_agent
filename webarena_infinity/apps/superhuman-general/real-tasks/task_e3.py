import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state["emails"]:
        if "Complete Your Survey" in e["subject"] and e["from"]["name"] == "SurveyMonkey":
            if e["isTrashed"] is True:
                return True, "The SurveyMonkey gift card email is in trash."
            return False, f"The SurveyMonkey gift card email is not in trash (isTrashed={e['isTrashed']})."

    return False, "Could not find the SurveyMonkey gift card email."
