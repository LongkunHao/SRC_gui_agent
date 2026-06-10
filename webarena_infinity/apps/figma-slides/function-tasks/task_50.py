import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    template_styles = state.get("templateStyles", [])
    for ts in template_styles:
        if ts.get("id") == "ts_001":
            text_styles = ts.get("textStyles", [])
            text_style_count = len(text_styles)

            if text_style_count != 4:
                return False, f"ts_001 has {text_style_count} text styles, expected 4."

            for txt in text_styles:
                if txt.get("name") == "Caption" or txt.get("id") == "txt_005":
                    return False, "Text style 'Caption' (txt_005) still exists in ts_001, expected it to be removed."

            return True, "ts_001 has 4 text styles and 'Caption' (txt_005) has been removed."

    return False, "Template style ts_001 not found in state."
