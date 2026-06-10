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
                if obj.get("id") == "obj_082":
                    responses = obj.get("responses", [])
                    response_count = len(responses)

                    if response_count != 6:
                        return False, f"Alignment obj_082 has {response_count} responses, expected 6."

                    found_user_001 = False
                    for r in responses:
                        if r.get("userId") == "user_001" and r.get("value") == 4:
                            found_user_001 = True
                            break

                    if not found_user_001:
                        return False, "No response from user_001 with value 4 found in alignment obj_082."

                    return True, "Alignment obj_082 has 6 responses including user_001 with value 4."
            return False, "Object obj_082 (alignment) not found on slide_009."

    return False, "Slide slide_009 ('Team Survey Results') not found in state."
