import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ms = next((m for m in state["milestones"] if "v1.2" in m["title"]), None)
    if ms:
        return False, "Milestone 'v1.2 — Hotfixes' still exists."

    # Side effect: issues 88, 89 should have milestoneId null
    issue88 = next((i for i in state["issues"] if i["id"] == 88), None)
    if issue88 and issue88["milestoneId"] == 7:
        return False, "Issue #88 still references deleted milestone."

    return True, "Milestone 'v1.2 — Hotfixes' deleted and references cleared."
