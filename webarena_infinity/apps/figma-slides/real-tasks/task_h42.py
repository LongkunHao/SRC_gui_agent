import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # James O'Brien commented about competitive comparison being outdated
    # He should be removed from collaborators
    for c in state.get("collaborators", []):
        if c.get("name") == "James O'Brien":
            errors.append("James O'Brien should have been removed from collaborators")
            break

    # Comparison Table header background should be #F24E1E
    for s in state.get("slides", []):
        if s.get("title") == "Competitive Landscape":
            for obj in s.get("objects", []):
                if obj.get("name") == "Comparison Table":
                    header_bg = obj.get("headerStyle", {}).get("background", "")
                    if header_bg.upper() != "#F24E1E":
                        errors.append(
                            f"Comparison Table header background is '{header_bg}', "
                            f"expected '#F24E1E'"
                        )
                    break
            break

    if errors:
        return False, "; ".join(errors)
    return True, "James O'Brien removed; comparison table header flagged #F24E1E"
