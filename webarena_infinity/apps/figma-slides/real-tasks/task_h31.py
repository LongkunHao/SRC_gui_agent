import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Feature adoption table on Data Comparison slide
    adoption_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Data Comparison":
            adoption_slide = s
            break

    if not adoption_slide:
        return False, "Could not find slide titled 'Data Comparison'"

    adoption_table = None
    for obj in adoption_slide.get("objects", []):
        if obj.get("name") == "Adoption Table":
            adoption_table = obj
            break

    if not adoption_table:
        return False, "Could not find 'Adoption Table' on Data Comparison slide"

    cells = adoption_table.get("cells", [])

    # Check no '--' values remain (was in cells[4][1] = AI Assist Q1 2025)
    for r, row in enumerate(cells):
        for c_idx, val in enumerate(row):
            if val == "--":
                errors.append(f"Adoption table cells[{r}][{c_idx}] is still '--', should be '0%'")

    # Competitive comparison table on Competitive Landscape slide
    comp_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Competitive Landscape":
            comp_slide = s
            break

    if not comp_slide:
        return False, "Could not find slide titled 'Competitive Landscape'"

    comp_table = None
    for obj in comp_slide.get("objects", []):
        if obj.get("name") == "Comparison Table":
            comp_table = obj
            break

    if not comp_table:
        return False, "Could not find 'Comparison Table' on Competitive Landscape slide"

    comp_cells = comp_table.get("cells", [])

    # Check no 'None' values remain (was in cells[2][3] = Design Tokens, Competitor B)
    # Check no 'Limited' values remain (was in cells[1][2] = Real-time Collab, Competitor A)
    for r, row in enumerate(comp_cells):
        for c_idx, val in enumerate(row):
            if val == "None":
                errors.append(f"Comparison table cells[{r}][{c_idx}] is still 'None', should be 'Planned'")
            if val == "Limited":
                errors.append(f"Comparison table cells[{r}][{c_idx}] is still 'Limited', should be 'Partial'")

    # Verify the specific expected values
    if len(comp_cells) > 2 and len(comp_cells[2]) > 3:
        if comp_cells[2][3] != "Planned":
            errors.append(f"Comparison cells[2][3] is '{comp_cells[2][3]}', expected 'Planned'")
    if len(comp_cells) > 1 and len(comp_cells[1]) > 2:
        if comp_cells[1][2] != "Partial":
            errors.append(f"Comparison cells[1][2] is '{comp_cells[1][2]}', expected 'Partial'")

    if errors:
        return False, "; ".join(errors)
    return True, "Adoption table '--' replaced with '0%'; comparison table 'None'->'Planned', 'Limited'->'Partial'"
