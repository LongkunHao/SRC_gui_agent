import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Q4 Roadmap":
            # Presenter notes
            notes = s.get("presenterNotes", "")
            expected_notes = "Key deliverables and milestones for Q4."
            if notes != expected_notes:
                errors.append(
                    f"Presenter notes are '{notes}', expected '{expected_notes}'"
                )

            for obj in s.get("objects", []):
                name = obj.get("name", "")

                if name == "Section Title":
                    rotation = obj.get("rotation")
                    if rotation != -5:
                        errors.append(
                            f"Section Title rotation is {rotation}, expected -5"
                        )
                    align = obj.get("textAlign")
                    if align != "left":
                        errors.append(
                            f"Section Title textAlign is '{align}', expected 'left'"
                        )

                elif name == "Section Subtitle":
                    opacity = obj.get("opacity")
                    if opacity != 60:
                        errors.append(
                            f"Section Subtitle opacity is {opacity}, expected 60"
                        )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Q4 Roadmap: notes updated, Section Title rotated -5 left, Subtitle opacity 60"
