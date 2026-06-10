import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("id") == "slide_016":
            objects = slide.get("objects", [])
            for obj in objects:
                if obj.get("id") == "obj_152":
                    stamps = obj.get("stamps", [])
                    stamp_count = len(stamps)

                    if stamp_count != 5:
                        return False, f"Stamps obj_152 has {stamp_count} stamps, expected 5."

                    found_user_001 = False
                    for stamp in stamps:
                        if stamp.get("userId") == "user_001" and stamp.get("type") == "thumbsUp":
                            found_user_001 = True
                            break

                    if not found_user_001:
                        return False, "No stamp from user_001 with type 'thumbsUp' found in obj_152."

                    return True, "Stamps obj_152 has 5 stamps including user_001 with 'thumbsUp'."
            return False, "Object obj_152 (stamps) not found on slide_016."

    return False, "Slide slide_016 ('Thank You') not found in state."
