import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        title = s.get("title", "")

        if title == "Competitive Landscape":
            for obj in s.get("objects", []):
                if obj.get("name") == "Comparison Table":
                    if obj.get("locked") is not True:
                        errors.append("Comparison Table should be locked")
                    break

        elif title == "Data Comparison":
            for obj in s.get("objects", []):
                if obj.get("name") == "Adoption Table":
                    fs = obj.get("fontSize")
                    if fs != 16:
                        errors.append(
                            f"Adoption Table fontSize is {fs}, expected 16"
                        )
                    break

    if errors:
        return False, "; ".join(errors)
    return True, "Comparison Table locked; Adoption Table fontSize set to 16"
