import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        title = s.get("title", "")
        layout = s.get("layout", "")

        if layout == "layout_title_content":
            for obj in s.get("objects", []):
                if obj.get("name") == "Title":
                    if obj.get("textAlign") != "center":
                        errors.append(
                            f"'{title}' Title textAlign is '{obj.get('textAlign')}', "
                            f"expected 'center'"
                        )
                    break

        elif layout == "layout_section":
            for obj in s.get("objects", []):
                if obj.get("name") == "Section Subtitle":
                    if obj.get("fontWeight") != 600:
                        errors.append(
                            f"'{title}' Section Subtitle fontWeight is "
                            f"{obj.get('fontWeight')}, expected 600"
                        )
                    if obj.get("fontSize") != 24:
                        errors.append(
                            f"'{title}' Section Subtitle fontSize is "
                            f"{obj.get('fontSize')}, expected 24"
                        )
                    break

    if errors:
        return False, "; ".join(errors)
    return True, "Title-content Titles centered; section Subtitle updated"
