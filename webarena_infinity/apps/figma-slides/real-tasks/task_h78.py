import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Q4 Planning has 5 slides (the most of any group)
    # Slides: Q4 Roadmap, Design System 2.0, API Reference,
    #         Team Survey Results, Data Comparison
    q4_planning_titles = {
        "Q4 Roadmap", "Design System 2.0", "API Reference",
        "Team Survey Results", "Data Comparison"
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in q4_planning_titles:
            if s.get("templateStyle") != "ts_002":
                errors.append(
                    f"'{title}' templateStyle is '{s.get('templateStyle')}', "
                    f"expected 'ts_002'"
                )
            for obj in s.get("objects", []):
                if obj.get("name") == "Title":
                    if obj.get("fontFamily") != "Plus Jakarta Sans":
                        errors.append(
                            f"'{title}' Title fontFamily is "
                            f"'{obj.get('fontFamily')}', "
                            f"expected 'Plus Jakarta Sans'"
                        )

    if errors:
        return False, "; ".join(errors)
    return True, "Largest group (Q4 Planning) set to Corporate Blue with Plus Jakarta Sans titles"
