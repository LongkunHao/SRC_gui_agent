import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Team Survey Results":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Team Survey Results'"

    objects = target.get("objects", [])

    # Find the poll object
    poll_obj = None
    alignment_obj = None
    for obj in objects:
        if obj.get("type") == "liveInteraction":
            if obj.get("interactionType") == "poll":
                poll_obj = obj
            elif obj.get("interactionType") == "alignment":
                alignment_obj = obj

    if poll_obj is None:
        return False, "Could not find poll interaction on Team Survey Results slide"

    # Check AI features option has votes > 15 (was 15)
    options = poll_obj.get("options", [])
    ai_option = None
    for opt in options:
        if opt.get("text") == "AI features":
            ai_option = opt
            break

    if ai_option is None:
        return False, "Could not find 'AI features' option in poll"

    ai_votes = ai_option.get("votes", 0)
    if ai_votes <= 15:
        return False, f"AI features has {ai_votes} votes, expected more than 15 (user should have voted)"

    # Check alignment object for user_001 response with value 5
    if alignment_obj is None:
        return False, "Could not find alignment interaction on Team Survey Results slide"

    responses = alignment_obj.get("responses", [])
    user_001_response = None
    for r in responses:
        if r.get("userId") == "user_001":
            user_001_response = r
            break

    if user_001_response is None:
        return False, "user_001 (Sarah Chen) has not submitted a response in the alignment survey"

    value = user_001_response.get("value")
    if value != 5:
        return False, f"user_001's alignment response value is {value}, expected 5"

    return True, "Voted for AI features in poll and submitted confidence 5 in alignment survey"
