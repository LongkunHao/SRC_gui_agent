import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    expected_notes = "Aiko will present the roadmap. Focus on timelines and deliverables."

    for slide in slides:
        if slide.get("title") == "Q4 Roadmap":
            notes = slide.get("presenterNotes", "")
            if notes == expected_notes:
                return True, "Slide 'Q4 Roadmap' has the correct presenterNotes."
            return False, f"Slide 'Q4 Roadmap' has presenterNotes '{notes}', expected '{expected_notes}'."

    return False, "No slide with title 'Q4 Roadmap' found."
