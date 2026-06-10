import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    template_styles = state.get("templateStyles", [])
    for ts in template_styles:
        if ts.get("id") == "ts_002":
            colors = ts.get("colors", [])
            for color in colors:
                if color.get("id") == "tc_013" or color.get("name") == "Primary":
                    value = color.get("value")
                    if value == "#0066FF":
                        return True, "Corporate Blue Primary color (tc_013) is correctly '#0066FF'."
                    else:
                        return False, f"Corporate Blue Primary color (tc_013) is '{value}', expected '#0066FF'."
            return False, "Primary color (tc_013) not found in Corporate Blue template style."

    return False, "Template style ts_002 (Corporate Blue) not found in state."
