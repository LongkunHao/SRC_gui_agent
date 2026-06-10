import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Q3 Review group slides: Q3 Highlights, Growth Metrics, Customer Feedback
    q3_titles = {"Q3 Highlights", "Growth Metrics"}
    # Customer Feedback has no "Title" object, only "Quote" and "Attribution"

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in q3_titles:
            title_obj = None
            for obj in s.get("objects", []):
                if obj.get("name") == "Title":
                    title_obj = obj
                    break
            if not title_obj:
                errors.append(f"No 'Title' object found on slide '{title}'")
                continue

            font = title_obj.get("fontFamily")
            if font != "Georgia":
                errors.append(f"'{title}' Title fontFamily is '{font}', expected 'Georgia'")

            weight = title_obj.get("fontWeight")
            if weight != 600:
                errors.append(f"'{title}' Title fontWeight is {weight}, expected 600")

    if errors:
        return False, "; ".join(errors)
    return True, "Q3 Review Title objects: fontFamily Georgia, fontWeight 600"
