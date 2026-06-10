import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Team Updates group slides: Resource Allocation, Sprint Timeline
    team_updates_titles = {"Resource Allocation", "Sprint Timeline"}

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in team_updates_titles:
            # Check template style
            ts = s.get("templateStyle")
            if ts != "ts_002":
                errors.append(f"'{title}' templateStyle is '{ts}', expected 'ts_002'")

            # Check background
            bg = s.get("background", {})
            if bg.get("type") != "solid":
                errors.append(f"'{title}' background type is '{bg.get('type')}', expected 'solid'")
            elif bg.get("color", "").upper() != "#FFFFFF":
                errors.append(f"'{title}' background color is '{bg.get('color')}', expected '#FFFFFF'")

            # Check transition
            trans = s.get("transition", {})
            if trans.get("type") != "move_in":
                errors.append(f"'{title}' transition type is '{trans.get('type')}', expected 'move_in'")
            if trans.get("direction") != "bottom":
                errors.append(f"'{title}' transition direction is '{trans.get('direction')}', expected 'bottom'")
            if trans.get("duration") != 400:
                errors.append(f"'{title}' transition duration is {trans.get('duration')}, expected 400")

    # Check Elena Kowalski is removed
    for c in state.get("collaborators", []):
        if c.get("name") == "Elena Kowalski":
            errors.append("Elena Kowalski should have been removed from collaborators")
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Team Updates: Corporate Blue, white bg, move_in bottom 400ms; Elena Kowalski removed"
