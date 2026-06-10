import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Presenter notes on Resource Allocation mention:
    # "Mobile team is borrowing 2 engineers from Platform"
    # Team C Card = Mobile App (borrowing) → stroke #FFAC33
    # Team B Card = Platform & API (lending) → stroke #FF6B6B

    for s in state.get("slides", []):
        if s.get("title") == "Resource Allocation":
            for obj in s.get("objects", []):
                name = obj.get("name", "")

                if name == "Team C Card":
                    stroke = obj.get("stroke")
                    if not stroke:
                        errors.append("Team C Card (borrowing) has no stroke")
                    elif stroke.get("color", "").upper() != "#FFAC33":
                        errors.append(
                            f"Team C Card stroke color is '{stroke.get('color')}', "
                            f"expected '#FFAC33'"
                        )

                elif name == "Team B Card":
                    stroke = obj.get("stroke")
                    if not stroke:
                        errors.append("Team B Card (lending) has no stroke")
                    elif stroke.get("color", "").upper() != "#FF6B6B":
                        errors.append(
                            f"Team B Card stroke color is '{stroke.get('color')}', "
                            f"expected '#FF6B6B'"
                        )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Borrowing team stroke #FFAC33; lending team stroke #FF6B6B"
