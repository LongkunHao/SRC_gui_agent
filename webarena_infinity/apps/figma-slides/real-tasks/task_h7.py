import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Competitive Landscape"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "Competitive Landscape":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Competitive Landscape'"

    # Find table object "Comparison Table"
    objects = target_slide.get("objects", [])
    table_obj = None
    for obj in objects:
        if obj.get("name") == "Comparison Table":
            table_obj = obj
            break

    if not table_obj:
        return False, "Could not find object named 'Comparison Table' on Competitive Landscape slide"

    cells = table_obj.get("cells", [])
    if len(cells) < 7:
        return False, f"Comparison Table has {len(cells)} rows, expected at least 7"

    # Check cells[2][2] == "Native" (Design Tokens, Competitor A)
    if len(cells[2]) > 2:
        val = cells[2][2]
        if val != "Native":
            errors.append(f"cells[2][2] (Design Tokens, Competitor A) is '{val}', expected 'Native'")
    else:
        errors.append(f"Row 2 has insufficient columns: {len(cells[2])}")

    # Check cells[4][3] == "In Beta" (AI Features, Competitor B)
    if len(cells[4]) > 3:
        val = cells[4][3]
        if val != "In Beta":
            errors.append(f"cells[4][3] (AI Features, Competitor B) is '{val}', expected 'In Beta'")
    else:
        errors.append(f"Row 4 has insufficient columns: {len(cells[4])}")

    # Check cells[5][1] == "$12/user/mo" (Pricing, DesignCraft)
    if len(cells[5]) > 1:
        val = cells[5][1]
        if val != "$12/user/mo":
            errors.append(f"cells[5][1] (Pricing, DesignCraft) is '{val}', expected '$12/user/mo'")
    else:
        errors.append(f"Row 5 has insufficient columns: {len(cells[5])}")

    if errors:
        return False, "; ".join(errors)
    return True, "Competitive comparison table updated: Competitor A Design Tokens=Native, Competitor B AI Features=In Beta, DesignCraft Pricing=$12/user/mo"
