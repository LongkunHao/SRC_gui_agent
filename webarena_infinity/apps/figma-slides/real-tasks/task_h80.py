import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # After changing cells ending in '0%' to '5%':
    expected_cells = [
        ["Feature", "Q1 2025", "Q2 2025", "Q3 2025", "Target Q4"],
        ["Real-time Collab", "68%", "72%", "81%", "95%"],
        ["Design Tokens", "12%", "25%", "41%", "65%"],
        ["Auto Layout", "45%", "52%", "58%", "75%"],
        ["AI Assist", "--", "8%", "22%", "45%"],
        ["Dev Handoff", "55%", "65%", "67%", "85%"],
    ]

    for s in state.get("slides", []):
        if s.get("title") == "Data Comparison":
            for obj in s.get("objects", []):
                if obj.get("name") == "Adoption Table":
                    cells = obj.get("cells", [])
                    for r in range(len(expected_cells)):
                        for c in range(len(expected_cells[r])):
                            if r < len(cells) and c < len(cells[r]):
                                if cells[r][c] != expected_cells[r][c]:
                                    errors.append(
                                        f"cells[{r}][{c}] is '{cells[r][c]}', "
                                        f"expected '{expected_cells[r][c]}'"
                                    )
                            else:
                                errors.append(f"Missing cell at [{r}][{c}]")
                    break
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Adoption table cells ending in '0%' changed to '5%'"
