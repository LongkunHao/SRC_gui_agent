import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state["emails"]:
        if e["subject"] == "FY2026 Budget Summary":
            if e["isStarred"] is False:
                return True, "The FY2026 Budget Summary email is unstarred."
            return False, f"The FY2026 Budget Summary email is still starred (isStarred={e['isStarred']})."

    return False, "Could not find the FY2026 Budget Summary email."
