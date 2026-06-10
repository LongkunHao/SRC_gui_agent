import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Q4 Planning group slides and their expected content-type changes:
    # - API Reference: code block → theme solarized
    # - Data Comparison: table → header bg #172B4D
    # - Team Survey Results: live interactions → hideResults true

    for s in state.get("slides", []):
        title = s.get("title", "")

        if title == "API Reference":
            for obj in s.get("objects", []):
                if obj.get("type") == "code":
                    theme = obj.get("theme")
                    if theme != "solarized":
                        errors.append(f"Code block theme is '{theme}', expected 'solarized'")

        elif title == "Data Comparison":
            for obj in s.get("objects", []):
                if obj.get("type") == "table":
                    header_bg = obj.get("headerStyle", {}).get("background", "")
                    if header_bg.upper() != "#172B4D":
                        errors.append(
                            f"Adoption Table header bg is '{header_bg}', expected '#172B4D'"
                        )

        elif title == "Team Survey Results":
            for obj in s.get("objects", []):
                if obj.get("type") == "liveInteraction":
                    itype = obj.get("interactionType", "")
                    if obj.get("hideResults") is not True:
                        errors.append(
                            f"Live interaction '{itype}' on Team Survey Results "
                            f"should have hideResults=true"
                        )

    if errors:
        return False, "; ".join(errors)
    return True, "Q4 Planning standardized: code→solarized, table header→#172B4D, interactions hidden"
