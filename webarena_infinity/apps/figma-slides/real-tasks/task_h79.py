import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Highest Target Q4 in seed: Real-time Collab at 90%
    # -> Competitive table cells[1][1] = 'Market Leader'
    # -> Adoption table cells[1][4] = '95%'

    # Check competitive table
    for s in state.get("slides", []):
        if s.get("title") == "Competitive Landscape":
            for obj in s.get("objects", []):
                if obj.get("name") == "Comparison Table":
                    cells = obj.get("cells", [])
                    if len(cells) > 1 and len(cells[1]) > 1:
                        if cells[1][1] != "Market Leader":
                            errors.append(
                                f"Comparison cells[1][1] is '{cells[1][1]}', "
                                f"expected 'Market Leader'"
                            )
                    break
            break

    # Check adoption table
    for s in state.get("slides", []):
        if s.get("title") == "Data Comparison":
            for obj in s.get("objects", []):
                if obj.get("name") == "Adoption Table":
                    cells = obj.get("cells", [])
                    if len(cells) > 1 and len(cells[1]) > 4:
                        if cells[1][4] != "95%":
                            errors.append(
                                f"Adoption cells[1][4] is '{cells[1][4]}', "
                                f"expected '95%'"
                            )
                    break
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Highest Target Q4 feature marked as Market Leader; target updated to 95%"
