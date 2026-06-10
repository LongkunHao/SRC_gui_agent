import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Slides that have an object named exactly "Title" (not "Section Title",
    # "Closing Title", etc.) should have color #A78BFA on that object.
    # Objects with other names should be untouched.

    for s in state.get("slides", []):
        slide_title = s.get("title", "")
        for obj in s.get("objects", []):
            name = obj.get("name", "")

            if name == "Title":
                color = obj.get("color", "")
                if color.upper() != "#A78BFA":
                    errors.append(
                        f"'{slide_title}' Title color is '{color}', expected '#A78BFA'"
                    )

    # Verify Section Title and Closing Title were NOT changed
    for s in state.get("slides", []):
        for obj in s.get("objects", []):
            name = obj.get("name", "")
            if name == "Section Title":
                color = obj.get("color", "")
                if color.upper() == "#A78BFA":
                    errors.append(
                        f"Section Title on '{s.get('title')}' should NOT have been "
                        f"changed to #A78BFA"
                    )
            elif name == "Closing Title":
                color = obj.get("color", "")
                if color.upper() == "#A78BFA":
                    errors.append(
                        f"Closing Title on '{s.get('title')}' should NOT have been "
                        f"changed to #A78BFA"
                    )

    if errors:
        return False, "; ".join(errors)
    return True, "All 'Title' objects set to #A78BFA; Section/Closing Title unchanged"
