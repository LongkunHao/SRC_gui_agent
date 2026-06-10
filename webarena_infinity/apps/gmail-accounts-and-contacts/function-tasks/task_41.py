import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    collaboration = state.get("accountSettings", {}).get("collaborationSettings", {})
    share_docs = collaboration.get("shareDocsInEmail")
    if share_docs is False:
        return True, "shareDocsInEmail is False."
    return False, f"shareDocsInEmail is {share_docs}, expected False."
