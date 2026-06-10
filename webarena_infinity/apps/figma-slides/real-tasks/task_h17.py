import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Data Comparison"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "Data Comparison":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Data Comparison'"

    # Find table object "Adoption Table"
    objects = target_slide.get("objects", [])
    table_obj = None
    for obj in objects:
        if obj.get("name") == "Adoption Table":
            table_obj = obj
            break

    if not table_obj:
        return False, "Could not find object named 'Adoption Table' on Data Comparison slide"

    cells = table_obj.get("cells", [])
    if len(cells) < 6:
        return False, f"Adoption Table has {len(cells)} rows, expected at least 6"

    # Q3 2025 column is index 3 (cols: Feature, Q1 2025, Q2 2025, Q3 2025, Target Q4)
    expected = {
        1: ("Real-time Collab", "86%"),
        2: ("Design Tokens", "46%"),
        3: ("Auto Layout", "63%"),
        4: ("AI Assist", "27%"),
        5: ("Dev Handoff", "72%"),
    }

    for row_idx, (feature_name, expected_val) in expected.items():
        if len(cells[row_idx]) <= 3:
            errors.append(f"Row {row_idx} ({feature_name}) has insufficient columns")
            continue
        actual = cells[row_idx][3]
        if actual != expected_val:
            errors.append(f"Row {row_idx} ({feature_name}) Q3 2025 value is '{actual}', expected '{expected_val}'")

    if errors:
        return False, "; ".join(errors)
    return True, "Q3 2025 adoption values increased by 5 points: 86%, 46%, 63%, 27%, 72%"
