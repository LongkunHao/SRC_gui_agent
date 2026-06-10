# Task: Remove delegates from VP of Product's company domain, add auto-saved HR as delegate.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    delegates = state.get("delegates", [])

    # Maya Patel (maya.patel@techcorp.io) should be removed (same domain as VP of Product Sarah Chen)
    for d in delegates:
        if d.get("email") == "maya.patel@techcorp.io":
            errors.append("Delegate maya.patel@techcorp.io should have been removed (same domain as VP of Product)")

    # hr@techcorp.io should be added as a delegate
    hr_delegate = None
    for d in delegates:
        if d.get("email") == "hr@techcorp.io":
            hr_delegate = d
            break

    if hr_delegate is None:
        errors.append("Delegate hr@techcorp.io not found (should have been added)")
    else:
        if hr_delegate.get("name") != "TechCorp HR Team":
            errors.append(
                f"New delegate name is '{hr_delegate.get('name')}' instead of 'TechCorp HR Team'"
            )

    # Other delegates should remain
    for email in ["laura.jm@gmail.com", "priya.sharma@cloudnine.dev", "jake.morrison@gmail.com"]:
        found = any(d.get("email") == email for d in delegates)
        if not found:
            errors.append(f"Delegate '{email}' should still exist")

    if errors:
        return False, "; ".join(errors)
    return True, "VP of Product company delegates removed, TechCorp HR Team added."
