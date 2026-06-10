import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("id") == "slide_009":
            objects = slide.get("objects", [])
            for obj in objects:
                if obj.get("id") == "obj_081":
                    options = obj.get("options", [])
                    for option in options:
                        if option.get("id") == "opt_02":
                            votes = option.get("votes")
                            if votes == 9:
                                return True, "Poll option opt_02 on obj_081 has 9 votes as expected."
                            else:
                                return False, f"Poll option opt_02 has {votes} votes, expected 9."
                    return False, "Option opt_02 not found in poll obj_081."
            return False, "Object obj_081 (poll) not found on slide_009."

    return False, "Slide slide_009 ('Team Survey Results') not found in state."
