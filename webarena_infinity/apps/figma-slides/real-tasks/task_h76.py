import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    accent_map = {
        "ts_001": "#FF6B35",  # Minimal Dark
        "ts_002": "#F7C948",  # Corporate Blue
        "ts_003": "#7B61FF",  # Warm Sunset
    }

    for ts in state.get("templateStyles", []):
        ts_id = ts.get("id")
        if ts_id in accent_map:
            expected_accent = accent_map[ts_id]
            for color in ts.get("colors", []):
                if color.get("name") == "Accent":
                    if color.get("value", "").upper() != expected_accent.upper():
                        errors.append(
                            f"{ts.get('name')} Accent is '{color.get('value')}', "
                            f"expected '{expected_accent}'"
                        )
                    break

        # Corporate Blue Heading 2 font size should be 28
        if ts_id == "ts_002":
            for text_style in ts.get("textStyles", []):
                if text_style.get("name") == "Heading 2":
                    if text_style.get("fontSize") != 28:
                        errors.append(
                            f"Corporate Blue Heading 2 fontSize is "
                            f"{text_style.get('fontSize')}, expected 28"
                        )
                    break

    if errors:
        return False, "; ".join(errors)
    return True, "Template accent colors updated; Corporate Blue Heading 2 resized"
