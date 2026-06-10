import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find template style - look for "Sunset Red" (renamed from "Warm Sunset")
    template_styles = state.get("templateStyles", state.get("templates", []))
    target_style = None

    if isinstance(template_styles, list):
        for ts in template_styles:
            ts_id = ts.get("id", "")
            ts_name = ts.get("name", "")
            if ts_id == "ts_003" or ts_name == "Sunset Red" or ts_name == "Warm Sunset":
                target_style = ts
                break
    elif isinstance(template_styles, dict):
        for ts_id, ts in template_styles.items():
            ts_name = ts.get("name", "")
            if ts_id == "ts_003" or ts_name == "Sunset Red" or ts_name == "Warm Sunset":
                target_style = ts
                break

    if not target_style:
        return False, "Could not find template style ts_003 (Warm Sunset / Sunset Red)"

    # Check name is "Sunset Red"
    if target_style.get("name") != "Sunset Red":
        errors.append(f"Template style name is '{target_style.get('name')}', expected 'Sunset Red'")

    # Find color named "Primary", check value is #E63946
    colors = target_style.get("colors", [])
    primary_found = False
    if isinstance(colors, list):
        for color in colors:
            if color.get("name") == "Primary":
                primary_found = True
                val = color.get("value", "")
                if val.upper() != "#E63946":
                    errors.append(f"Primary color value is '{val}', expected '#E63946'")
                break
    elif isinstance(colors, dict):
        for cid, color in colors.items():
            if color.get("name") == "Primary" or cid == "tc_023":
                primary_found = True
                val = color.get("value", "")
                if val.upper() != "#E63946":
                    errors.append(f"Primary color value is '{val}', expected '#E63946'")
                break

    if not primary_found:
        errors.append("Primary color not found in template style colors")

    # Check no text style named "Caption"
    text_styles = target_style.get("textStyles", [])
    if isinstance(text_styles, list):
        for ts in text_styles:
            if ts.get("name") == "Caption":
                errors.append("Text style 'Caption' should have been removed but still exists")
                break
    elif isinstance(text_styles, dict):
        for ts_id, ts in text_styles.items():
            name = ts.get("name", "") if isinstance(ts, dict) else ""
            if name == "Caption" or ts_id == "txt_025":
                errors.append("Text style 'Caption' should have been removed but still exists")
                break

    if errors:
        return False, "; ".join(errors)
    return True, "Template renamed to 'Sunset Red', Primary color updated to #E63946, Caption text style removed"
