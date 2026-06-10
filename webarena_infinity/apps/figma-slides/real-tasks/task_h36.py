import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find Data Comparison slide
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Data Comparison":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Data Comparison'"

    table_obj = None
    for obj in target_slide.get("objects", []):
        if obj.get("name") == "Adoption Table":
            table_obj = obj
            break

    if not table_obj:
        return False, "Could not find 'Adoption Table' on Data Comparison slide"

    cells = table_obj.get("cells", [])
    if len(cells) < 6:
        return False, f"Adoption Table has {len(cells)} rows, expected at least 6"

    # After swapping Q2 (col 2) and Q3 (col 3), expected values:
    expected = {
        (1, 2): "81%", (1, 3): "72%",   # Real-time Collab
        (2, 2): "41%", (2, 3): "25%",   # Design Tokens
        (3, 2): "58%", (3, 3): "52%",   # Auto Layout
        (4, 2): "22%", (4, 3): "8%",    # AI Assist
        (5, 2): "67%", (5, 3): "60%",   # Dev Handoff
    }

    for (r, c), expected_val in expected.items():
        if len(cells[r]) > c:
            actual = cells[r][c]
            if actual != expected_val:
                errors.append(f"cells[{r}][{c}] is '{actual}', expected '{expected_val}'")
        else:
            errors.append(f"Row {r} has insufficient columns")

    if errors:
        return False, "; ".join(errors)
    return True, "Feature adoption table Q2/Q3 columns swapped correctly"
