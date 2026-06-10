import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Two epics share the performance label (id 4):
    #   Epic 3 (Performance Optimization Phase 2) — created 2026-02-10
    #   Epic 9 (Search Infrastructure Upgrade)    — created 2026-02-28
    # Epic 9 is newer, so it should be closed.

    epic9 = next((e for e in state["epics"] if e["id"] == 9), None)
    if epic9 is None:
        return False, "Epic 'Search Infrastructure Upgrade' (id 9) not found."
    if epic9.get("status") != "closed":
        return False, f"Epic 9 status is '{epic9.get('status')}', expected 'closed'."

    # Epic 3 should now contain the children of epic 9 (#60, #61, #62)
    epic3 = next((e for e in state["epics"] if e["id"] == 3), None)
    if epic3 is None:
        return False, "Epic 'Performance Optimization Phase 2' (id 3) not found."

    for issue_id in [60, 61, 62]:
        if issue_id not in epic3.get("childIssueIds", []):
            return False, (
                f"Issue #{issue_id} not in epic 3 childIssueIds: "
                f"{epic3.get('childIssueIds')}."
            )

    return True, "Epic 9 closed, its children moved to epic 3."
