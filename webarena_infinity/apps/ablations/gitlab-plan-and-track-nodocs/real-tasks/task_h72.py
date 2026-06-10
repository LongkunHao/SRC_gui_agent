import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Two open issues assigned to both Jun (4) and Emily (8): #15 and #30.
    # #15 belongs to epic 4 (Mobile Responsive Redesign) — this is the target.
    issue = next((i for i in state["issues"] if i["id"] == 15), None)
    if issue is None:
        return False, "Issue #15 not found."

    critical_id = next(l["id"] for l in state["labels"] if l["name"] == "priority::critical")
    priority_ids = {l["id"] for l in state["labels"] if l["name"].startswith("priority::")}

    if critical_id not in issue.get("labelIds", []):
        return False, (
            f"Issue #15 does not have priority::critical. "
            f"Labels: {issue.get('labelIds')}."
        )

    other_priority = [l for l in issue.get("labelIds", [])
                      if l in priority_ids and l != critical_id]
    if other_priority:
        return False, f"Issue #15 has extra priority labels: {other_priority}."

    if issue.get("timeEstimate") != 144000:
        return False, (
            f"Issue #15 timeEstimate is {issue.get('timeEstimate')}, "
            f"expected 144000 (40 hours)."
        )

    return True, "Issue #15 set to priority::critical with 40h time estimate."
