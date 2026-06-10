import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        title = s.get("title", "")
        bg = s.get("background", {})
        is_gradient = bg.get("type") == "gradient"
        is_skipped = s.get("skipped") is True

        if is_gradient or is_skipped:
            if s.get("slideNumberEnabled") is not False:
                reason = "gradient bg" if is_gradient else "skipped"
                errors.append(
                    f"'{title}' slideNumberEnabled should be False ({reason})"
                )
        else:
            if s.get("slideNumberEnabled") is not True:
                errors.append(
                    f"'{title}' slideNumberEnabled should be True"
                )
            if s.get("slideNumberFormat") != "padded":
                errors.append(
                    f"'{title}' slideNumberFormat is '{s.get('slideNumberFormat')}', "
                    f"expected 'padded'"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Slide numbers conditionally set: gradient/skipped disabled, others padded"
