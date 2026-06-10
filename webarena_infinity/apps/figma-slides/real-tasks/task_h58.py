import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    deck = state.get("deckSettings", {})

    # Default template style → Warm Sunset (ts_003)
    dts = deck.get("defaultTemplateStyle")
    if dts != "ts_003":
        errors.append(f"Default template style is '{dts}', expected 'ts_003'")

    # Default transition → slide_out, bottom, bounce, 500ms
    dt = deck.get("defaultTransition", {})
    if dt.get("type") != "slide_out":
        errors.append(f"Default transition type is '{dt.get('type')}', expected 'slide_out'")
    if dt.get("direction") != "bottom":
        errors.append(
            f"Default transition direction is '{dt.get('direction')}', expected 'bottom'"
        )
    if dt.get("easing") != "bounce":
        errors.append(f"Default transition easing is '{dt.get('easing')}', expected 'bounce'")
    if dt.get("duration") != 500:
        errors.append(f"Default transition duration is {dt.get('duration')}, expected 500")

    # All slides with templateStyle ts_001 (Minimal Dark) should have
    # slideNumberFormat = "with_total"
    # In seed data, ALL 16 slides use ts_001
    for s in state.get("slides", []):
        title = s.get("title", "")
        ts = s.get("templateStyle", "")
        if ts == "ts_001":
            fmt = s.get("slideNumberFormat")
            if fmt != "with_total":
                errors.append(
                    f"'{title}' slideNumberFormat is '{fmt}', expected 'with_total'"
                )

    if errors:
        return False, "; ".join(errors)
    return True, (
        "Deck defaults: Warm Sunset, slide_out/bottom/bounce/500ms; "
        "Minimal Dark slides: with_total format"
    )
