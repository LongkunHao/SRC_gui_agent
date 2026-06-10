import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides = state.get("slides", [])

    # Find the group that represents "Q3 Review"
    # First, find the groupId by looking for slides with groupName containing "Q3"
    q3_group_id = None
    groups = state.get("groups", state.get("slideGroups", []))

    # Try to find group by name in groups list
    if isinstance(groups, list):
        for g in groups:
            if "Q3" in g.get("name", ""):
                q3_group_id = g.get("id")
                break
    elif isinstance(groups, dict):
        for gid, g in groups.items():
            name = g.get("name", "") if isinstance(g, dict) else ""
            if "Q3" in name:
                q3_group_id = gid
                break

    # Also find Q3 Review slides by checking slide-level groupName
    q3_slides = []
    for s in slides:
        group_name = s.get("groupName") or ""
        group_id = s.get("groupId")
        if "Q3" in group_name or (q3_group_id and group_id == q3_group_id):
            q3_slides.append(s)

    if not q3_slides:
        return False, "No slides found in Q3 Review group"

    for s in q3_slides:
        title = s.get("title", "unknown")
        ts = s.get("templateStyle", "")
        if ts != "ts_002":
            errors.append(f"Slide '{title}' templateStyle is '{ts}', expected 'ts_002' (Corporate Blue)")

        bg = s.get("background", {})
        bg_type = bg.get("type", "")
        bg_color = bg.get("color", "")
        if bg_type != "solid":
            errors.append(f"Slide '{title}' background type is '{bg_type}', expected 'solid'")
        if bg_color.upper() != "#FFFFFF":
            errors.append(f"Slide '{title}' background color is '{bg_color}', expected '#FFFFFF'")

    if errors:
        return False, "; ".join(errors)
    return True, f"All {len(q3_slides)} Q3 Review slides have Corporate Blue style and white backgrounds"
