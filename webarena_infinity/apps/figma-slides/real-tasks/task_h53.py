import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Team Survey Results":
            for obj in s.get("objects", []):
                name = obj.get("name", "")

                if name == "Title":
                    # The winning option is "AI features" with 15 votes
                    expected_text = "Team Survey Results \u2014 AI features"
                    text = obj.get("text", "")
                    if text != expected_text:
                        errors.append(
                            f"Title text is '{text}', expected '{expected_text}'"
                        )

                elif obj.get("type") == "liveInteraction" and \
                        obj.get("interactionType") == "poll":
                    question = obj.get("question", "")
                    if question != "Q4 Priorities (Closed)":
                        errors.append(
                            f"Poll question is '{question}', "
                            f"expected 'Q4 Priorities (Closed)'"
                        )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Title updated with winning poll option; poll question set to closed"
