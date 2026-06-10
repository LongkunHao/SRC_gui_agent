import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Check no library named "Presentation Icons Pack"
    libraries = state.get("libraries", [])
    for lib in libraries:
        lib_name = lib.get("name", "")
        if "Presentation Icons Pack" in lib_name:
            errors.append(f"Library 'Presentation Icons Pack' should have been removed, but still exists")

    # Find "DesignCraft Component Library", check enabled == False
    designcraft_found = False
    for lib in libraries:
        lib_name = lib.get("name", "")
        if "DesignCraft Component Library" in lib_name:
            designcraft_found = True
            if lib.get("enabled") is not False:
                errors.append(f"DesignCraft Component Library enabled is {lib.get('enabled')}, expected False")

    if not designcraft_found:
        errors.append("DesignCraft Component Library not found in libraries")

    # Find slide "Competitive Landscape" and get its ID
    slides = state.get("slides", [])
    comp_slide_id = None
    for s in slides:
        if s.get("title") == "Competitive Landscape":
            comp_slide_id = s.get("id")
            break

    if not comp_slide_id:
        errors.append("Could not find slide titled 'Competitive Landscape' to verify comments")
    else:
        # Check no comment has this slideId
        comments = state.get("comments", [])
        for c in comments:
            if c.get("slideId") == comp_slide_id:
                errors.append(f"Comment {c.get('id', 'unknown')} still references Competitive Landscape slide ({comp_slide_id})")

    if errors:
        return False, "; ".join(errors)
    return True, "Presentation Icons Pack removed, DesignCraft Component Library disabled, comments on Competitive Landscape deleted"
