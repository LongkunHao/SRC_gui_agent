import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Design System 2.0":
            # Seed animations:
            # Title: null (no change expected)
            # Content: slide_up -> remove, opacity 90
            # Timeline Badge: pop -> remove, opacity 85
            # GA Badge: pop -> remove, opacity 85
            expected = {
                "Title": {"animation": None, "opacity": 100},
                "Content": {"animation": None, "opacity": 90},
                "Timeline Badge": {"animation": None, "opacity": 85},
                "GA Badge": {"animation": None, "opacity": 85},
            }

            for obj in s.get("objects", []):
                name = obj.get("name", "")
                if name in expected:
                    exp = expected[name]
                    if obj.get("animation") is not None:
                        errors.append(
                            f"'{name}' still has animation, expected None"
                        )
                    if obj.get("opacity") != exp["opacity"]:
                        errors.append(
                            f"'{name}' opacity is {obj.get('opacity')}, "
                            f"expected {exp['opacity']}"
                        )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Design System 2.0 animations removed; opacity set by prior style"
