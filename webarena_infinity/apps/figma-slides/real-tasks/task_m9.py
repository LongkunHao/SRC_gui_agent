import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Data Comparison":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Data Comparison'"

    # Find the table object named "Adoption Table"
    table_obj = None
    for obj in target.get("objects", []):
        if obj.get("name") == "Adoption Table":
            table_obj = obj
            break

    if table_obj is None:
        return False, "Could not find object named 'Adoption Table' on Data Comparison slide"

    cells = table_obj.get("cells", [])

    # Check cells[1][3] == "85%" (Real-time Collab, Q3 2025)
    if len(cells) < 2 or len(cells[1]) < 4:
        return False, f"Table does not have enough rows/columns: {len(cells)} rows"

    rtc_q3 = cells[1][3]
    if rtc_q3 != "85%":
        return False, f"Real-time Collab Q3 2025 value is '{rtc_q3}', expected '85%'"

    # Check cells[2][4] == "65%" (Design Tokens, Target Q4)
    if len(cells) < 3 or len(cells[2]) < 5:
        return False, f"Table does not have enough rows/columns for Design Tokens row"

    dt_q4 = cells[2][4]
    if dt_q4 != "65%":
        return False, f"Design Tokens Target Q4 value is '{dt_q4}', expected '65%'"

    return True, "Table updated: Real-time Collab Q3='85%', Design Tokens Target Q4='65%'"
