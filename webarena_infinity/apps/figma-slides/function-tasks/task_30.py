import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_013":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_013' not found."

    objects = slide.get("objects", [])
    table_obj = None
    for obj in objects:
        if obj.get("id") == "obj_121":
            table_obj = obj
            break
    if table_obj is None:
        return False, "Table object 'obj_121' not found on slide_013."

    columns = table_obj.get("columns")
    if columns is None:
        # Fall back to checking first row length
        cells = table_obj.get("cells", [])
        if len(cells) > 0:
            columns = len(cells[0])
        else:
            return False, "Table has no cells to determine column count."

    if columns == 5:
        return True, "Table columns correctly updated to 5."
    else:
        return False, f"Table columns is {columns}, expected 5."
