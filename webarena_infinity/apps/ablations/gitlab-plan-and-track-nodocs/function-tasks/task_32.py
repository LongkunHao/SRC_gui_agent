import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    label = next((l for l in state["labels"] if l["name"] == "needs-investigation"), None)
    if label:
        return False, "Label 'needs-investigation' still exists."

    # Side effect: label id 19 should be removed from issue #41
    issue41 = next((i for i in state["issues"] if i["id"] == 41), None)
    if issue41 and 19 in issue41["labelIds"]:
        return False, "Label id 19 still present on issue #41 after label deletion."

    return True, "Label 'needs-investigation' deleted and removed from issues."
