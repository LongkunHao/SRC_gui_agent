import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Q4 Planning group slides: Q4 Roadmap, Design System 2.0, API Reference,
    # Team Survey Results, Data Comparison
    q4_titles = {
        "Design System 2.0", "API Reference",
        "Team Survey Results", "Data Comparison"
    }
    # Q4 Roadmap has "Section Title" not "Title", so skip it

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in q4_titles:
            title_obj = None
            for obj in s.get("objects", []):
                if obj.get("name") == "Title":
                    title_obj = obj
                    break

            if not title_obj:
                errors.append(f"No 'Title' object found on slide '{title}'")
                continue

            anim = title_obj.get("animation")
            if anim is None:
                errors.append(f"'{title}' Title has no animation, expected pop")
                continue

            if anim.get("style") != "pop":
                errors.append(f"'{title}' Title animation style is '{anim.get('style')}', expected 'pop'")
            if anim.get("duration") != 300:
                errors.append(f"'{title}' Title animation duration is {anim.get('duration')}, expected 300")
            if anim.get("timing") != "on_click":
                errors.append(f"'{title}' Title animation timing is '{anim.get('timing')}', expected 'on_click'")

    if errors:
        return False, "; ".join(errors)
    return True, "Q4 Planning Title objects: pop animation 300ms on_click added where missing"
