import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Resource Allocation":
            team_a = None
            team_c = None
            for obj in s.get("objects", []):
                if obj.get("name") == "Team A Card":
                    team_a = obj
                elif obj.get("name") == "Team C Card":
                    team_c = obj

            if not team_a:
                return False, "Team A Card not found"
            if not team_c:
                return False, "Team C Card not found"

            # Team A (8 engineers, most) -> stroke color gold
            stroke_a = team_a.get("stroke", {})
            if not stroke_a or stroke_a.get("color", "").upper() != "#F7C948":
                errors.append(
                    f"Team A Card stroke color is "
                    f"'{stroke_a.get('color') if stroke_a else 'none'}', "
                    f"expected '#F7C948'"
                )

            # Team C (4 engineers, fewest) -> fill #1A1A2E
            if team_c.get("fill", "").upper() != "#1A1A2E":
                errors.append(
                    f"Team C Card fill is '{team_c.get('fill')}', expected '#1A1A2E'"
                )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Largest team card has gold stroke; smallest team card fill updated"
