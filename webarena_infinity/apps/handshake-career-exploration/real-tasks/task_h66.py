"""
Task: Pivot career interests toward healthcare: set career community to
'Healthcare', replace all roles with 'Solutions Architect' and 'Research
Scientist', replace all industries with 'Healthcare Technology' and
'Biotechnology', and add 'Supply Chain' to job functions. Save.

Verify:
(1) careerCommunity == 'Healthcare'
(2) roles == ['Solutions Architect', 'Research Scientist'] (order flexible)
(3) industries == ['Healthcare Technology', 'Biotechnology'] (order flexible)
(4) 'Supply Chain' in jobFunctions
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    ci = state.get("currentUser", {}).get("careerInterests", {})
    errors = []

    # Check 1: Career community
    if ci.get("careerCommunity") != "Healthcare":
        errors.append(
            f"careerCommunity should be 'Healthcare', "
            f"got '{ci.get('careerCommunity')}'."
        )

    # Check 2: Roles replaced
    roles = set(ci.get("roles", []))
    expected_roles = {"Solutions Architect", "Research Scientist"}
    if roles != expected_roles:
        errors.append(
            f"roles should be exactly {expected_roles}, got {roles}."
        )

    # Check 3: Industries replaced
    industries = set(ci.get("industries", []))
    expected_industries = {"Healthcare Technology", "Biotechnology"}
    if industries != expected_industries:
        errors.append(
            f"industries should be exactly {expected_industries}, got {industries}."
        )

    # Check 4: Supply Chain in job functions
    if "Supply Chain" not in ci.get("jobFunctions", []):
        errors.append(
            f"'Supply Chain' not in jobFunctions. "
            f"Current: {ci.get('jobFunctions')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Healthcare career pivot complete: community='Healthcare', "
        "roles={Solutions Architect, Research Scientist}, "
        "industries={Healthcare Technology, Biotechnology}, "
        "Supply Chain in job functions."
    )
