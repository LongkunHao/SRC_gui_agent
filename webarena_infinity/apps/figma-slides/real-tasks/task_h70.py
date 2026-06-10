import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    q3_review_titles = {"Q3 Highlights", "Growth Metrics", "Customer Feedback"}

    for s in state.get("slides", []):
        if s.get("title") not in q3_review_titles:
            continue

        slide_title = s["title"]
        for obj in s.get("objects", []):
            if obj.get("type") != "text":
                continue

            name = obj.get("name", "")
            anim = obj.get("animation")

            if slide_title == "Q3 Highlights" and name == "Title":
                # Had no animation -> should get fade 400ms after_previous
                if not anim:
                    errors.append(f"Q3 Highlights Title has no animation, expected fade")
                else:
                    if anim.get("style") != "fade":
                        errors.append(f"Q3 Highlights Title animation style is '{anim.get('style')}', expected 'fade'")
                    if anim.get("duration") != 400:
                        errors.append(f"Q3 Highlights Title animation duration is {anim.get('duration')}, expected 400")
                    if anim.get("timing") != "after_previous":
                        errors.append(f"Q3 Highlights Title animation timing is '{anim.get('timing')}', expected 'after_previous'")

            elif slide_title == "Growth Metrics":
                # All text objects had no animation -> should get fade 400ms after_previous
                if not anim:
                    errors.append(f"Growth Metrics '{name}' has no animation, expected fade")
                else:
                    if anim.get("style") != "fade":
                        errors.append(f"Growth Metrics '{name}' animation style is '{anim.get('style')}', expected 'fade'")
                    if anim.get("duration") != 400:
                        errors.append(f"Growth Metrics '{name}' animation duration is {anim.get('duration')}, expected 400")
                    if anim.get("timing") != "after_previous":
                        errors.append(f"Growth Metrics '{name}' animation timing is '{anim.get('timing')}', expected 'after_previous'")

            elif slide_title == "Customer Feedback":
                # Quote had fade 600ms -> duration should be 600 (already matches)
                # Attribution had fade 300ms -> duration should be 600
                if not anim:
                    errors.append(f"Customer Feedback '{name}' has no animation")
                elif anim.get("duration") != 600:
                    errors.append(
                        f"Customer Feedback '{name}' animation duration is "
                        f"{anim.get('duration')}, expected 600"
                    )

    if errors:
        return False, "; ".join(errors)
    return True, "Q3 Review text animations added/updated correctly"
