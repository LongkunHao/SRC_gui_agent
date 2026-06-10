import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check Healthcare theme exists
    themes = state.get("brandingThemes", [])
    hc_theme = next((t for t in themes if t.get("name") == "Healthcare"), None)
    if hc_theme is None:
        return False, "'Healthcare' branding theme not found."

    if "Net 60" not in hc_theme.get("paymentTerms", ""):
        return False, f"Expected 'Net 60' in payment terms, got '{hc_theme.get('paymentTerms')}'."

    hc_theme_id = hc_theme.get("id")

    # Check Summit Health repeating invoice uses Healthcare theme
    rep = next(
        (r for r in state.get("repeatingInvoices", []) if r.get("id") == "rep_005"),
        None
    )
    if rep is None:
        return False, "Summit Health repeating invoice (rep_005) not found."

    if rep.get("brandingThemeId") != hc_theme_id:
        return False, f"Summit Health repeating invoice should use 'Healthcare' theme."

    return True, f"Healthcare theme created with Net 60 days, Summit Health repeating invoice updated to use it."
