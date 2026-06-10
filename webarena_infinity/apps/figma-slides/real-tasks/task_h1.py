import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Q3 Highlights"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "Q3 Highlights":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Q3 Highlights'"

    objects = target_slide.get("objects", [])

    # Find metric cards by name
    card_map = {}
    for obj in objects:
        name = obj.get("name", "")
        if name in ("Metric Card 1", "Metric Card 2", "Metric Card 3"):
            card_map[name] = obj

    for card_name in ("Metric Card 1", "Metric Card 2", "Metric Card 3"):
        if card_name not in card_map:
            errors.append(f"Object '{card_name}' not found on Q3 Highlights slide")

    if errors:
        return False, "; ".join(errors)

    # Check Card 1: text contains "2.8M" and "+40%"
    card1 = card_map["Metric Card 1"]
    card1_text = card1.get("text", "")
    if "2.8M" not in card1_text:
        errors.append(f"Metric Card 1 text does not contain '2.8M', got: {card1_text!r}")
    if "+40%" not in card1_text:
        errors.append(f"Metric Card 1 text does not contain '+40%', got: {card1_text!r}")

    # Check Card 2: text contains "$22.3M" and "+35%"
    card2 = card_map["Metric Card 2"]
    card2_text = card2.get("text", "")
    if "$22.3M" not in card2_text:
        errors.append(f"Metric Card 2 text does not contain '$22.3M', got: {card2_text!r}")
    if "+35%" not in card2_text:
        errors.append(f"Metric Card 2 text does not contain '+35%', got: {card2_text!r}")

    # Check all three fills == "#383838"
    for card_name in ("Metric Card 1", "Metric Card 2", "Metric Card 3"):
        card = card_map[card_name]
        fill = card.get("fill", "")
        if fill.upper() != "#383838":
            errors.append(f"{card_name} fill is {fill!r}, expected '#383838'")

    if errors:
        return False, "; ".join(errors)
    return True, "Q3 metric cards updated correctly: Card 1 has 2.8M/+40%, Card 2 has $22.3M/+35%, all fills #383838"
