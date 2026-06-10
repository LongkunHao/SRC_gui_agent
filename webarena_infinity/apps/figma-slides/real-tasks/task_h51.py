import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    reverse_map = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}

    # Expected reversed directions based on seed data:
    # slide_003 (Q3 Highlights): push left → right
    # slide_004 (Growth Metrics): slide_in right → left
    # slide_006 (Q4 Roadmap): push left → right
    # slide_011 (Resource Allocation): move_in bottom → top
    # slide_014 (Key Risks): slide_in left → right
    expected = {
        "Q3 Highlights": "right",
        "Growth Metrics": "left",
        "Q4 Roadmap": "right",
        "Resource Allocation": "top",
        "Key Risks & Mitigations": "right",
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in expected:
            trans = s.get("transition", {})
            direction = trans.get("direction")
            if direction != expected[title]:
                errors.append(
                    f"'{title}' direction is '{direction}', expected '{expected[title]}'"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "All directional transitions reversed"
