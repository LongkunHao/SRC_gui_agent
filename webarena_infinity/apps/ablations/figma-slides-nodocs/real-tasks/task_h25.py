import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Toggle starred on every presentation tagged 'quarterly'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Tagged 'quarterly': pres_001 (was starred → should be unstarred),
    #                      pres_012 (was unstarred → should be starred)
    errors = []

    if "pres_001" not in pres_map:
        errors.append("pres_001 not found")
    else:
        p = pres_map["pres_001"]
        if p.get("starred", False):
            errors.append(
                f"pres_001 ({p.get('title')}) was originally starred and should now "
                f"be unstarred, but starred=={p.get('starred')}"
            )

    if "pres_012" not in pres_map:
        errors.append("pres_012 not found")
    else:
        p = pres_map["pres_012"]
        if not p.get("starred", False):
            errors.append(
                f"pres_012 ({p.get('title')}) was originally unstarred and should now "
                f"be starred, but starred=={p.get('starred')}"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Starred status toggled on both 'quarterly' presentations: "
        "pres_001 unstarred, pres_012 starred."
    )
