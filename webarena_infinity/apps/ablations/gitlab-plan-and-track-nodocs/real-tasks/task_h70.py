import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sprint7 = next(
        (it for it in state["iterations"] if it.get("title") == "Sprint 7"), None
    )
    if sprint7 is None:
        return False, "Sprint 7 not found."
    s7_id = sprint7["id"]

    # Open Sprint 7 issues with timeEstimate > 0 and original timeSpent == 0:
    # #2, #8, #12, #16, #19, #23, #32, #36, #45, #55, #73, #76, #102
    expected = {
        2: 11700,    # 46800 * 0.25
        8: 11700,
        12: 11700,
        16: 7200,    # 28800 * 0.25
        19: 7200,
        23: 7200,
        32: 4500,    # 18000 * 0.25
        36: 4500,
        45: 3600,    # 14400 * 0.25
        55: 7200,
        73: 2700,    # 10800 * 0.25
        76: 4500,
        102: 2700,
    }

    for issue_id, exp_spent in expected.items():
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("timeSpent") != exp_spent:
            return False, (
                f"Issue #{issue_id} timeSpent is {issue.get('timeSpent')}, "
                f"expected {exp_spent}."
            )

    return True, "25% of time estimate logged for Sprint 7 issues with no prior time spent."
