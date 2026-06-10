import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    expected_gradient = {
        "type": "gradient",
        "gradient": {
            "type": "linear",
            "angle": 180,
            "stops": [
                {"color": "#0A0A2A", "position": 0},
                {"color": "#1E1E1E", "position": 100},
            ],
        },
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        has_animation = any(
            obj.get("animation") is not None for obj in s.get("objects", [])
        )
        bg = s.get("background", {})

        if has_animation:
            if bg.get("type") != "gradient":
                errors.append(f"'{title}' background type is '{bg.get('type')}', expected 'gradient'")
            else:
                grad = bg.get("gradient", {})
                stops = grad.get("stops", [])
                if len(stops) < 2:
                    errors.append(f"'{title}' gradient has {len(stops)} stops, expected 2")
                else:
                    if stops[0].get("color", "").upper() != "#0A0A2A":
                        errors.append(f"'{title}' gradient stop 0 color is '{stops[0].get('color')}', expected '#0A0A2A'")
                    if stops[1].get("color", "").upper() != "#1E1E1E":
                        errors.append(f"'{title}' gradient stop 1 color is '{stops[1].get('color')}', expected '#1E1E1E'")
        else:
            if bg.get("type") != "solid":
                errors.append(f"'{title}' background type is '{bg.get('type')}', expected 'solid'")
            elif bg.get("color", "").upper() != "#2C2C2C":
                errors.append(f"'{title}' background color is '{bg.get('color')}', expected '#2C2C2C'")

    if errors:
        return False, "; ".join(errors)
    return True, "Animated slides have gradient bg; non-animated slides have solid #2C2C2C"
