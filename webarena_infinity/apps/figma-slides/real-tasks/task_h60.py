import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Shapes with cornerRadius in seed data and expected new values:
    # Metric Card 1 (12→16), Metric Card 2 (12→16), Metric Card 3 (12→16)
    # Team A Card (12→16), Team B Card (12→16), Team C Card (12→16)
    # Risk 1 (8→12), Risk 2 (8→12), Risk 3 (8→12)
    expected_radius = {
        "Metric Card 1": 16, "Metric Card 2": 16, "Metric Card 3": 16,
        "Team A Card": 16, "Team B Card": 16, "Team C Card": 16,
        "Risk 1": 12, "Risk 2": 12, "Risk 3": 12,
    }

    # Shapes with "Status" in text → fontWeight 700
    # Team A Card, Team B Card, Team C Card all have "Status:" in their text
    status_shapes = {"Team A Card", "Team B Card", "Team C Card"}

    for s in state.get("slides", []):
        for obj in s.get("objects", []):
            name = obj.get("name", "")

            if name in expected_radius:
                cr = obj.get("cornerRadius")
                if cr != expected_radius[name]:
                    errors.append(
                        f"'{name}' cornerRadius is {cr}, expected {expected_radius[name]}"
                    )

            if name in status_shapes:
                fw = obj.get("fontWeight")
                if fw != 700:
                    errors.append(f"'{name}' fontWeight is {fw}, expected 700")

    if errors:
        return False, "; ".join(errors)
    return True, "Corner radii increased by 4; shapes with 'Status' bolded to 700"
