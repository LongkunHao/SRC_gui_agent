import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = next((s for s in slides if s.get("id") == "slide_013"), None)
    if not slide:
        return False, "Slide slide_013 not found."

    objects = slide.get("objects", [])
    obj = next((o for o in objects if o.get("id") == "obj_121"), None)
    if not obj:
        return False, "Object obj_121 (table) not found on slide_013."

    cells = obj.get("cells", [])
    if len(cells) <= 4:
        return False, f"Table obj_121 has only {len(cells)} rows, expected at least 5 (need row index 4)."

    row = cells[4]
    if len(row) < 2:
        return False, f"Row 4 has only {len(row)} columns, expected at least 2."

    value = row[1]
    if value != "Advanced":
        return False, f"Expected cells[4][1] (AI Features, DesignCraft col) to be 'Advanced', but found '{value}'."

    return True, "Table obj_121 cells[4][1] is 'Advanced' as expected."
