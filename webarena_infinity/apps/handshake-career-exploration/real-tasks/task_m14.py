import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    grad_date = state.get("currentUser", {}).get("careerInterests", {}).get("expectedGraduationDate", "")

    if grad_date == "August 2027":
        return True, f"Expected graduation date successfully changed to 'August 2027'."

    return False, (
        f"Expected graduation date is '{grad_date}', expected 'August 2027'."
    )
