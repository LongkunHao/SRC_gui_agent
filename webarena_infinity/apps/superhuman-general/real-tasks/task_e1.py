import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state["emails"]:
        if e["subject"] == "Re: Series B Term Sheet Discussion" and e["from"]["name"] == "Emily Rodriguez":
            if e["isStarred"] is True:
                return True, "The term sheet email from Emily Rodriguez is starred."
            return False, f"The term sheet email from Emily Rodriguez is not starred (isStarred={e['isStarred']})."

    return False, "Could not find the term sheet email from Emily Rodriguez."
