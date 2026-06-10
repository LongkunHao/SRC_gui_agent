import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Professional Services theme ID
    prof_theme = next(
        (t for t in state.get("brandingThemes", []) if "Professional" in t.get("name", "")),
        None
    )
    if prof_theme is None:
        return False, "Professional Services branding theme not found."

    prof_id = prof_theme.get("id")

    # All active repeating invoices should use Professional Services
    active_ris = [r for r in state.get("repeatingInvoices", []) if r.get("status") == "active"]
    if len(active_ris) == 0:
        return False, "No active repeating invoices found."

    for ri in active_ris:
        if ri.get("brandingThemeId") != prof_id:
            return False, f"Repeating invoice {ri.get('id')} uses theme '{ri.get('brandingThemeId')}', expected '{prof_id}'."

    return True, f"All {len(active_ris)} active repeating invoices now use Professional Services theme."
