import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []
    deck = state.get("deckSettings", {})

    # Check default template style is Corporate Blue (ts_002)
    default_style = deck.get("defaultTemplateStyle")
    if default_style != "ts_002":
        errors.append(f"Default template style is '{default_style}', expected 'ts_002'")

    # Check default transition
    trans = deck.get("defaultTransition", {})
    if trans.get("type") != "move_in":
        errors.append(f"Default transition type is '{trans.get('type')}', expected 'move_in'")
    if trans.get("direction") != "top":
        errors.append(f"Default transition direction is '{trans.get('direction')}', expected 'top'")
    if trans.get("easing") != "ease_in":
        errors.append(f"Default transition easing is '{trans.get('easing')}', expected 'ease_in'")

    # Check slide number format
    fmt = deck.get("slideNumberFormat")
    if fmt != "with_total":
        errors.append(f"Slide number format is '{fmt}', expected 'with_total'")

    if errors:
        return False, "; ".join(errors)
    return True, "Deck settings: Corporate Blue default, move_in/top/ease_in transition, with_total slide numbers"
