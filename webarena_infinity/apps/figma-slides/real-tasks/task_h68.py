import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Seed data shapes and their original strokes:
    # With stroke: Team A/B/C Cards (width 2), Risk 1/2/3 (width 1) -> +1
    # Without stroke (null): Accent Line, Metric Cards 1/2/3, Timeline Badge, GA Badge -> new {#404040, 1}
    expected = {
        "Accent Line": {"color": "#404040", "width": 1},
        "Metric Card 1": {"color": "#404040", "width": 1},
        "Metric Card 2": {"color": "#404040", "width": 1},
        "Metric Card 3": {"color": "#404040", "width": 1},
        "Timeline Badge": {"color": "#404040", "width": 1},
        "GA Badge": {"color": "#404040", "width": 1},
        "Team A Card": {"color": "#7B61FF", "width": 3},
        "Team B Card": {"color": "#0ACF83", "width": 3},
        "Team C Card": {"color": "#F24E1E", "width": 3},
        "Risk 1": {"color": "#F24E1E", "width": 2},
        "Risk 2": {"color": "#FFAC33", "width": 2},
        "Risk 3": {"color": "#0ACF83", "width": 2},
    }

    for s in state.get("slides", []):
        for obj in s.get("objects", []):
            if obj.get("type") == "shape" and obj.get("name") in expected:
                name = obj["name"]
                exp = expected[name]
                stroke = obj.get("stroke")
                if not stroke:
                    errors.append(f"'{name}' has no stroke, expected {exp}")
                else:
                    if stroke.get("color", "").upper() != exp["color"].upper():
                        errors.append(
                            f"'{name}' stroke color is '{stroke.get('color')}', "
                            f"expected '{exp['color']}'"
                        )
                    if stroke.get("width") != exp["width"]:
                        errors.append(
                            f"'{name}' stroke width is {stroke.get('width')}, "
                            f"expected {exp['width']}"
                        )

    if errors:
        return False, "; ".join(errors)
    return True, "All shape strokes updated correctly"
