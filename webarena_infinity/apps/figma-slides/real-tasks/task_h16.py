import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides = state.get("slides", [])
    if not slides:
        return False, "No slides found in state"

    # Check all slides have slideNumberEnabled == True and slideNumberFormat == "with_total"
    for s in slides:
        title = s.get("title", s.get("id", "unknown"))

        if s.get("slideNumberEnabled") is not True:
            errors.append(f"Slide '{title}' slideNumberEnabled is {s.get('slideNumberEnabled')}, expected True")

        fmt = s.get("slideNumberFormat", "")
        if fmt != "with_total":
            errors.append(f"Slide '{title}' slideNumberFormat is '{fmt}', expected 'with_total'")

    # Check aspect ratio
    deck_settings = state.get("deckSettings", state.get("deck", {}))
    aspect = deck_settings.get("aspectRatio", "")
    if aspect != "4:3":
        errors.append(f"deckSettings.aspectRatio is '{aspect}', expected '4:3'")

    if errors:
        return False, "; ".join(errors)
    return True, f"All {len(slides)} slides have slide numbers enabled with 'with_total' format, aspect ratio set to 4:3"
