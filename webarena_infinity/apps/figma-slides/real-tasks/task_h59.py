import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Growth Metrics":
            # Right Column: fontWeight 700, fontSize 18
            for obj in s.get("objects", []):
                if obj.get("name") == "Right Column":
                    fw = obj.get("fontWeight")
                    if fw != 700:
                        errors.append(
                            f"Right Column fontWeight is {fw}, expected 700"
                        )
                    fs = obj.get("fontSize")
                    if fs != 18:
                        errors.append(
                            f"Right Column fontSize is {fs}, expected 18"
                        )
                    break

            # Presenter notes
            notes = s.get("presenterNotes", "")
            expected = "Enterprise growth is our Q4 focus area."
            if notes != expected:
                errors.append(f"Presenter notes are '{notes}', expected '{expected}'")
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Right Column: weight 700, size 18; presenter notes updated"
