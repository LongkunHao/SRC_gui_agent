import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])

    # Find slides that were in Q4 Planning group (group_002)
    # These should now have groupName "Product Roadmap"
    q4_slides = []
    for slide in slides:
        group_name = slide.get("groupName")
        if group_name in ("Q4 Planning", "Product Roadmap"):
            q4_slides.append(slide)

    if len(q4_slides) == 0:
        return False, "Could not find any slides in 'Q4 Planning' or 'Product Roadmap' group"

    # Check all of them have groupName "Product Roadmap"
    wrong_name = []
    for slide in q4_slides:
        if slide.get("groupName") != "Product Roadmap":
            wrong_name.append(f"'{slide.get('title')}' has groupName '{slide.get('groupName')}'")

    if wrong_name:
        return False, f"Some slides still have old group name: {'; '.join(wrong_name)}"

    # Find Q4 Roadmap slide (the section divider) and check background
    roadmap_slide = None
    for slide in slides:
        if slide.get("title") == "Q4 Roadmap":
            roadmap_slide = slide
            break

    if roadmap_slide is None:
        return False, "Could not find slide with title 'Q4 Roadmap'"

    bg = roadmap_slide.get("background", {})
    bg_type = bg.get("type")
    if bg_type != "solid":
        return False, f"Q4 Roadmap background type is '{bg_type}', expected 'solid'"

    bg_color = bg.get("color", "")
    if bg_color.upper() != "#0D1B2A":
        return False, f"Q4 Roadmap background color is '{bg_color}', expected '#0D1B2A'"

    return True, "Group renamed to 'Product Roadmap' and Q4 Roadmap background set to #0D1B2A"
