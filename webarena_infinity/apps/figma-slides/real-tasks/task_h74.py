import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # "Let Aiko take over" is in Q4 Roadmap presenter notes
    # "hiring timeline" is in Key Risks presenter notes
    for s in state.get("slides", []):
        title = s.get("title", "")

        if title == "Q4 Roadmap":
            trans = s.get("transition", {})
            if trans.get("type") != "smart_animate":
                errors.append(
                    f"Q4 Roadmap transition type is '{trans.get('type')}', "
                    f"expected 'smart_animate'"
                )
            if trans.get("easing") != "ease_in_out":
                errors.append(
                    f"Q4 Roadmap easing is '{trans.get('easing')}', "
                    f"expected 'ease_in_out'"
                )
            if trans.get("duration") != 600:
                errors.append(
                    f"Q4 Roadmap duration is {trans.get('duration')}, expected 600"
                )

        elif title == "Key Risks & Mitigations":
            if s.get("skipped") is not True:
                errors.append("Key Risks & Mitigations should be skipped")

    if errors:
        return False, "; ".join(errors)
    return True, "Presenter-notes-based changes applied correctly"
