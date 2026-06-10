import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Sprint Planning organizer is nate.patel@acmecorp.com
    # His sprint retrospective email is "Re: Sprint 23 Retrospective Notes"
    for e in state.get("emails", []):
        if (e["subject"] == "Re: Sprint 23 Retrospective Notes"
                and e["from"]["email"] == "nate.patel@acmecorp.com"):
            if e.get("isTrashed", False):
                return True, "Sprint retrospective email from Nate Patel (Sprint Planning organizer) has been trashed."
            return False, f"Sprint retrospective email from Nate Patel found but not trashed (isTrashed={e.get('isTrashed')})."

    return False, "Could not find 'Re: Sprint 23 Retrospective Notes' from nate.patel@acmecorp.com."
