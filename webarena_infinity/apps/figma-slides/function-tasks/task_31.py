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
    row_count = len(cells)
    if row_count != 6:
        return False, f"Expected table obj_121 to have 6 rows (last row deleted), but found {row_count}."

    return True, "Table obj_121 on slide_013 has 6 rows as expected (last row was deleted)."
