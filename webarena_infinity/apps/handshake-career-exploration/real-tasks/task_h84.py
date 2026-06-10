"""
Task: Follow every employer who sent you a message but doesn't host any upcoming events.

Discovery:
Employers who messaged: Google(emp_01), Anthropic(emp_15), Meta(emp_07),
  McKinsey(emp_04), Microsoft(emp_03), Stripe(emp_10), Amazon(emp_09),
  Apple(emp_05), JPMorgan(emp_02), Salesforce(emp_19), Bain(emp_11), Tesla(emp_12).
Employers with upcoming events: McKinsey(emp_04), Meta(emp_07), Google(emp_01),
  Anthropic(emp_15), JPMorgan(emp_02), Salesforce(emp_19).
Messaged but no upcoming events:
  Microsoft(emp_03 already followed), Stripe(emp_10 already followed),
  Amazon(emp_09 NOT followed), Apple(emp_05 already followed),
  Bain(emp_11 NOT followed), Tesla(emp_12 already followed).

Verify:
(1) emp_09 in followedEmployerIds
(2) emp_11 in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])
    errors = []

    # Check 1: Amazon followed
    if "emp_09" not in followed:
        errors.append(
            f"Amazon (emp_09) not in followedEmployerIds. "
            f"Currently following: {followed}"
        )

    # Check 2: Bain followed
    if "emp_11" not in followed:
        errors.append(
            f"Bain (emp_11) not in followedEmployerIds. "
            f"Currently following: {followed}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Amazon (emp_09) and Bain (emp_11) followed. These are the messaged "
        "employers without upcoming events that were not already followed."
    )
