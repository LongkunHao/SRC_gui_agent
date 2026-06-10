import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Metric Card 3 on Q3 Highlights shows uptime below SLA target
    # Should have a 2px #F24E1E stroke
    for s in state.get("slides", []):
        if s.get("title") == "Q3 Highlights":
            for obj in s.get("objects", []):
                if obj.get("name") == "Metric Card 3":
                    stroke = obj.get("stroke")
                    if not stroke:
                        errors.append("Metric Card 3 has no stroke")
                    else:
                        if stroke.get("color", "").upper() != "#F24E1E":
                            errors.append(
                                f"Metric Card 3 stroke color is '{stroke.get('color')}', "
                                f"expected '#F24E1E'"
                            )
                        if stroke.get("width") != 2:
                            errors.append(
                                f"Metric Card 3 stroke width is {stroke.get('width')}, "
                                f"expected 2"
                            )
            break

    # Marcus's comment about uptime on Q3 Highlights should be resolved
    for c in state.get("comments", []):
        if c.get("userName") == "Marcus Rivera" and "uptime" in c.get("text", "").lower():
            if c.get("resolved") is not True:
                errors.append("Marcus's uptime comment should be resolved")

    if errors:
        return False, "; ".join(errors)
    return True, "Metric Card 3 flagged with #F24E1E stroke; uptime comment resolved"
