import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Thank You":
            for obj in s.get("objects", []):
                if obj.get("name") == "Closing Title":
                    text = obj.get("text", "")
                    if text != "Questions & Discussion":
                        errors.append(
                            f"Closing Title text is '{text}', "
                            f"expected 'Questions & Discussion'"
                        )
                    fw = obj.get("fontWeight")
                    if fw != 800:
                        errors.append(
                            f"Closing Title fontWeight is {fw}, expected 800"
                        )

                elif obj.get("name") == "Reaction Stamps":
                    if obj.get("visible") is not False:
                        errors.append("Reaction Stamps should be hidden (visible=false)")

            break

    if errors:
        return False, "; ".join(errors)
    return True, "Closing Title updated to 'Questions & Discussion' weight 800; stamps hidden"
