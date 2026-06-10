import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Open CI/CD Pipeline Modernization children:
    # #19 (w8), #20 (w5), #21 (w8), #53 (w8), #54 (w13)
    # estimate = weight * 2 hours (in seconds), spent = estimate / 2
    expected = {
        19: (57600, 28800),   # 8*2h=16h=57600s, half=28800s
        20: (36000, 18000),   # 5*2h=10h=36000s, half=18000s
        21: (57600, 28800),
        53: (57600, 28800),
        54: (93600, 46800),   # 13*2h=26h=93600s, half=46800s
    }

    for issue_id, (exp_est, exp_spent) in expected.items():
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("timeEstimate") != exp_est:
            return False, (
                f"Issue #{issue_id} timeEstimate is {issue.get('timeEstimate')}, "
                f"expected {exp_est}."
            )
        if issue.get("timeSpent") != exp_spent:
            return False, (
                f"Issue #{issue_id} timeSpent is {issue.get('timeSpent')}, "
                f"expected {exp_spent}."
            )

    return True, "CI/CD epic children have correct time estimates and time spent."
