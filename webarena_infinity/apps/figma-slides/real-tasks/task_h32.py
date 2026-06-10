import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Feature adoption table is on "Data Comparison" slide
    data_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Data Comparison":
            data_slide = s
            break

    if not data_slide:
        return False, "Could not find slide titled 'Data Comparison'"

    adoption_table = None
    for obj in data_slide.get("objects", []):
        if obj.get("name") == "Adoption Table":
            adoption_table = obj
            break

    if not adoption_table:
        return False, "Could not find 'Adoption Table' on Data Comparison slide"

    # Check locked
    if not adoption_table.get("locked", False):
        errors.append("Adoption Table is not locked")

    # Competitive comparison table is on "Competitive Landscape" slide
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

    # Check header background
    header_style = comp_table.get("headerStyle", {})
    bg = header_style.get("background", "").upper()
    if bg != "#0052CC":
        errors.append(f"Comparison Table header background is '{bg}', expected '#0052CC'")

    if errors:
        return False, "; ".join(errors)
    return True, "Adoption Table locked; Comparison Table header background #0052CC"
