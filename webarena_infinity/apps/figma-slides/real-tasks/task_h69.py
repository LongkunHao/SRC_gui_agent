import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find competitive comparison table
    comp_table = None
    for s in state.get("slides", []):
        if s.get("title") == "Competitive Landscape":
            for obj in s.get("objects", []):
                if obj.get("name") == "Comparison Table":
                    comp_table = obj
                    break
            break

    if not comp_table:
        return False, "Comparison Table not found on Competitive Landscape slide"

    cells = comp_table.get("cells", [])

    # cells[1][1] should be 'Full (81%)' (Real-time Collab, DesignCraft)
    if len(cells) > 1 and len(cells[1]) > 1:
        if cells[1][1] != "Full (81%)":
            errors.append(
                f"Comparison cells[1][1] is '{cells[1][1]}', expected 'Full (81%)'"
            )
    else:
        errors.append("Comparison table has insufficient rows/columns")

    # cells[2][1] should be 'Native (41%)' (Design Tokens, DesignCraft)
    if len(cells) > 2 and len(cells[2]) > 1:
        if cells[2][1] != "Native (41%)":
            errors.append(
                f"Comparison cells[2][1] is '{cells[2][1]}', expected 'Native (41%)'"
            )
    else:
        errors.append("Comparison table has insufficient rows/columns")

    if errors:
        return False, "; ".join(errors)
    return True, "Competitive table cross-referenced with adoption Q3 values"
