import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    group_slides = [s for s in slides if s.get("groupId") == "group_001"]

    if not group_slides:
        return False, "No slides found with groupId 'group_001'."

    expected_name = "Q3 Performance Review"
    for slide in group_slides:
        name = slide.get("groupName", "")
        if name != expected_name:
            return False, (
                f"Slide '{slide.get('title')}' in group_001 has groupName '{name}', "
                f"expected '{expected_name}'."
            )

    return True, f"All {len(group_slides)} slides in group_001 have groupName '{expected_name}'."
