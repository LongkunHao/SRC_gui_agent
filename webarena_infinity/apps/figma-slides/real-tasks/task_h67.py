import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides_with_interactions = set()

    for s in state.get("slides", []):
        title = s.get("title", "")
        for obj in s.get("objects", []):
            if obj.get("type") == "liveInteraction":
                slides_with_interactions.add(s.get("id"))
                if obj.get("visible") is not False:
                    errors.append(
                        f"'{obj.get('name')}' on '{title}' visible is "
                        f"{obj.get('visible')}, expected False"
                    )

    # Slides with interactions should have dissolve at 800ms
    for s in state.get("slides", []):
        if s.get("id") in slides_with_interactions:
            trans = s.get("transition", {})
            if trans.get("type") != "dissolve":
                errors.append(
                    f"'{s.get('title')}' transition type is '{trans.get('type')}', "
                    f"expected 'dissolve'"
                )
            if trans.get("duration") != 800:
                errors.append(
                    f"'{s.get('title')}' transition duration is {trans.get('duration')}, "
                    f"expected 800"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "All live interactions hidden; affected slides have dissolve at 800ms"
