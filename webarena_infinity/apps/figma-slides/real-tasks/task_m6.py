import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    template_styles = state.get("templateStyles", [])

    # Find the template that was "Minimal Dark" (now should be "Dark Mode Pro")
    target = None
    for ts in template_styles:
        if ts.get("name") == "Dark Mode Pro":
            target = ts
            break

    if target is None:
        # Check if it's still named "Minimal Dark"
        for ts in template_styles:
            if ts.get("name") == "Minimal Dark":
                return False, "Template is still named 'Minimal Dark', expected 'Dark Mode Pro'"
        return False, "Could not find template named 'Dark Mode Pro' or 'Minimal Dark'"

    # Find the Primary color in this template
    colors = target.get("colors", [])
    primary = None
    for color in colors:
        if color.get("name") == "Primary":
            primary = color
            break

    if primary is None:
        return False, "Could not find color named 'Primary' in Dark Mode Pro template"

    primary_value = primary.get("value", "")
    if primary_value.upper() != "#6C5CE7":
        return False, f"Primary color is '{primary_value}', expected '#6C5CE7'"

    return True, "Template renamed to 'Dark Mode Pro' with Primary color #6C5CE7"
