import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Key Risks & Mitigations":
            for obj in s.get("objects", []):
                name = obj.get("name", "")

                if name == "Risk 1":
                    fill = obj.get("fill", "")
                    if fill.upper() != "#5C1010":
                        errors.append(f"Risk 1 fill is '{fill}', expected '#5C1010'")

                elif name == "Risk 2":
                    fill = obj.get("fill", "")
                    if fill.upper() != "#5C3D10":
                        errors.append(f"Risk 2 fill is '{fill}', expected '#5C3D10'")

                elif name == "Risk 3":
                    fill = obj.get("fill", "")
                    if fill.upper() != "#0D3D1A":
                        errors.append(
                            f"Risk 3 fill is '{fill}', expected '#0D3D1A' (unchanged)"
                        )

            # Check transition: push top, spring, 500ms
            trans = s.get("transition", {})
            if trans.get("type") != "push":
                errors.append(
                    f"Transition type is '{trans.get('type')}', expected 'push'"
                )
            if trans.get("direction") != "top":
                errors.append(
                    f"Transition direction is '{trans.get('direction')}', expected 'top'"
                )
            if trans.get("easing") != "spring":
                errors.append(
                    f"Transition easing is '{trans.get('easing')}', expected 'spring'"
                )
            if trans.get("duration") != 500:
                errors.append(
                    f"Transition duration is {trans.get('duration')}, expected 500"
                )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Risk cards: HIGH→#5C1010, MED→#5C3D10, LOW unchanged; push top spring 500ms"
