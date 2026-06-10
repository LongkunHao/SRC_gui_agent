import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides = state.get("slides", [])

    # Ungrouped slides are those with groupId == null/None
    ungrouped_titles = []
    for s in slides:
        group_id = s.get("groupId")
        if group_id is None:
            ungrouped_titles.append(s.get("title", "unknown"))
            ts = s.get("templateStyle", "")
            if ts != "ts_002":
                errors.append(f"Ungrouped slide '{s.get('title', 'unknown')}' templateStyle is '{ts}', expected 'ts_002' (Corporate Blue)")

    if not ungrouped_titles:
        errors.append("No ungrouped slides found (slides with groupId==null)")

    # Check deck default template style
    deck_settings = state.get("deckSettings", state.get("deck", {}))
    default_ts = deck_settings.get("defaultTemplateStyle", "")
    if default_ts != "ts_002":
        errors.append(f"deckSettings.defaultTemplateStyle is '{default_ts}', expected 'ts_002'")

    if errors:
        return False, "; ".join(errors)
    return True, f"Corporate Blue applied to {len(ungrouped_titles)} ungrouped slides and set as deck default"
