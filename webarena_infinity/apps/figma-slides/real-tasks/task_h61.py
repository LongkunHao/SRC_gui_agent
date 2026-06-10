import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    group_specs = {
        "Q3 Review": {"type": "smart_animate", "direction": None, "easing": "ease_in_out", "duration": 500},
        "Q4 Planning": {"type": "push", "direction": "left", "easing": "spring", "duration": 600},
        "Team Updates": {"type": "move_in", "direction": "bottom", "easing": "bounce", "duration": 400},
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        group = s.get("groupName")
        trans = s.get("transition", {})

        if group in group_specs:
            spec = group_specs[group]
            for key, expected in spec.items():
                actual = trans.get(key)
                if key == "direction" and expected is None:
                    continue
                if actual != expected:
                    errors.append(
                        f"'{title}' transition {key} is '{actual}', expected '{expected}'"
                    )
        else:
            if trans.get("type") != "dissolve":
                errors.append(
                    f"'{title}' transition type is '{trans.get('type')}', expected 'dissolve'"
                )
            if trans.get("easing") != "ease":
                errors.append(
                    f"'{title}' easing is '{trans.get('easing')}', expected 'ease'"
                )
            if trans.get("duration") != 400:
                errors.append(
                    f"'{title}' duration is {trans.get('duration')}, expected 400"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "All group-based transitions standardized correctly"
