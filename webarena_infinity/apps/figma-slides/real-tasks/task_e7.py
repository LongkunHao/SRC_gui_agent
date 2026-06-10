import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])

    # Find slides that belong to the Q3 Review group (originally group_001)
    # We look for slides that were in that group by checking known titles
    q3_titles = {"Q3 Highlights", "Growth Metrics", "Customer Feedback"}
    group_slides = [s for s in slides if s.get("title") in q3_titles]

    if len(group_slides) == 0:
        # Try to find by groupName in case titles were not changed
        group_slides = [s for s in slides if s.get("groupName") == "Q3 Performance"]

    if len(group_slides) == 0:
        return False, "Could not find any slides belonging to the Q3 Review group"

    for slide in group_slides:
        group_name = slide.get("groupName")
        if group_name != "Q3 Performance":
            return False, f"Slide '{slide.get('title')}' has groupName '{group_name}', expected 'Q3 Performance'"

    return True, "Q3 Review group renamed to 'Q3 Performance'"
