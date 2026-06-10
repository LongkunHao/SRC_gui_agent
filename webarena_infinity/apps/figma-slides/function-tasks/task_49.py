import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    template_styles = state.get("templateStyles", [])
    for ts in template_styles:
        if ts.get("id") == "ts_003":
            colors = ts.get("colors", [])
            color_count = len(colors)
            if color_count != 7:
                return False, f"Warm Sunset has {color_count} colors, expected 7."

            found_highlight = False
            for color in colors:
                if color.get("name") == "Highlight" and color.get("value") == "#FFD700":
                    found_highlight = True
                    break

            if not found_highlight:
                return False, "No color with name 'Highlight' and value '#FFD700' found in Warm Sunset."

            return True, "Warm Sunset has 7 colors and includes 'Highlight' (#FFD700)."

    return False, "Template style ts_003 (Warm Sunset) not found in state."
