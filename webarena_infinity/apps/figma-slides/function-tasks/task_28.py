import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_010":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_010' not found."

    objects = slide.get("objects", [])
    table_obj = None
    for obj in objects:
        if obj.get("id") == "obj_091":
            table_obj = obj
            break
    if table_obj is None:
        return False, "Table object 'obj_091' not found on slide_010."

    cells = table_obj.get("cells", [])
    if len(cells) < 2:
        return False, f"Table has {len(cells)} rows, expected at least 2."

    row = cells[1]
    if len(row) < 5:
        return False, f"Row 1 has {len(row)} columns, expected at least 5."

    value = row[4]
    if value == "95%":
        return True, "Table cell cells[1][4] correctly updated to '95%'."
    else:
        return False, f"Table cell cells[1][4] is '{value}', expected '95%'."
