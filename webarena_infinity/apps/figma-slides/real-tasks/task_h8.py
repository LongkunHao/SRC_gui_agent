import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Check deck name
    deck_settings = state.get("deckSettings", state.get("deck", {}))
    deck_name = deck_settings.get("name", deck_settings.get("title", ""))
    if deck_name != "Q4 2025 Product Roadmap":
        errors.append(f"Deck name is '{deck_name}', expected 'Q4 2025 Product Roadmap'")

    slides = state.get("slides", [])

    # Find slides that were in Q4 Planning group, check groupName is now "Product Roadmap"
    # Q4 Planning slides: Q4 Roadmap, Design System 2.0, API Reference, Team Survey Results, Data Comparison
    q4_titles = ["Q4 Roadmap", "Design System 2.0", "API Reference", "Team Survey Results", "Data Comparison"]
    found_q4_slides = False
    for s in slides:
        title = s.get("title", "")
        group_name = s.get("groupName", "")
        if title in q4_titles:
            found_q4_slides = True
            if group_name != "Product Roadmap":
                errors.append(f"Slide '{title}' groupName is '{group_name}', expected 'Product Roadmap'")

    # Also check groups list if present
    groups = state.get("groups", state.get("slideGroups", []))
    if isinstance(groups, list):
        for g in groups:
            if g.get("id") == "group_002" or "Q4" in g.get("name", ""):
                if g.get("name") != "Product Roadmap":
                    errors.append(f"Group '{g.get('name')}' should be renamed to 'Product Roadmap'")
    elif isinstance(groups, dict):
        for gid, g in groups.items():
            if gid == "group_002" or "Q4" in g.get("name", ""):
                if g.get("name") != "Product Roadmap":
                    errors.append(f"Group '{g.get('name')}' should be renamed to 'Product Roadmap'")

    if not found_q4_slides:
        errors.append("Could not find any Q4 Planning slides to verify group rename")

    # Find slide "Q4 Roadmap", find "Section Title" object, check text == "Product Roadmap"
    roadmap_slide = None
    for s in slides:
        if s.get("title") == "Q4 Roadmap":
            roadmap_slide = s
            break

    if not roadmap_slide:
        errors.append("Could not find slide titled 'Q4 Roadmap'")
    else:
        objects = roadmap_slide.get("objects", [])
        section_title_obj = None
        for obj in objects:
            if obj.get("name") == "Section Title":
                section_title_obj = obj
                break
        if not section_title_obj:
            errors.append("Could not find 'Section Title' object on Q4 Roadmap slide")
        else:
            text = section_title_obj.get("text", "")
            if text != "Product Roadmap":
                errors.append(f"Section Title text is '{text}', expected 'Product Roadmap'")

    if errors:
        return False, "; ".join(errors)
    return True, "Deck renamed to 'Q4 2025 Product Roadmap', Q4 Planning group renamed to 'Product Roadmap', section title updated"
