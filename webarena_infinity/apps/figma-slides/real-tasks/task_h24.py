import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find Q3 Highlights slide
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Q3 Highlights":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Q3 Highlights'"

    card_map = {}
    for obj in target_slide.get("objects", []):
        name = obj.get("name", "")
        if name in ("Metric Card 1", "Metric Card 2", "Metric Card 3"):
            card_map[name] = obj

    for card_name in ("Metric Card 1", "Metric Card 2", "Metric Card 3"):
        if card_name not in card_map:
            errors.append(f"Object '{card_name}' not found")

    if errors:
        return False, "; ".join(errors)

    # Cards 1 and 2 contain "YoY" in seed data -> should have stroke
    for card_name in ("Metric Card 1", "Metric Card 2"):
        card = card_map[card_name]
        stroke = card.get("stroke")
        if stroke is None:
            errors.append(f"{card_name} has no stroke, expected 2px #0ACF83")
            continue
        stroke_color = stroke.get("color", "").upper()
        if stroke_color != "#0ACF83":
            errors.append(f"{card_name} stroke color is '{stroke_color}', expected '#0ACF83'")
        stroke_width = stroke.get("width")
        if stroke_width != 2:
            errors.append(f"{card_name} stroke width is {stroke_width}, expected 2")

    # Card 3 contains "SLA" in seed data -> fill should be #F24E1E
    card3 = card_map["Metric Card 3"]
    fill = card3.get("fill", "").upper()
    if fill != "#F24E1E":
        errors.append(f"Metric Card 3 fill is '{fill}', expected '#F24E1E'")

    if errors:
        return False, "; ".join(errors)
    return True, "YoY cards have 2px #0ACF83 stroke; SLA card fill is #F24E1E"
