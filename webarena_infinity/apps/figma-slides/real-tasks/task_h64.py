import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    for s in state.get("slides", []):
        if s.get("title") == "Key Risks & Mitigations":
            risk1 = None
            risk3 = None
            for obj in s.get("objects", []):
                if obj.get("name") == "Risk 1":
                    risk1 = obj
                elif obj.get("name") == "Risk 3":
                    risk3 = obj

            if not risk1:
                return False, "Risk 1 not found"
            if not risk3:
                return False, "Risk 3 not found"

            # After swap: Risk 1 (HIGH) gets LOW's color, Risk 3 (LOW) gets HIGH's color
            # Seed: Risk 1 fill=#3D1010, Risk 3 fill=#0D3D1A
            if risk1.get("fill") != "#0D3D1A":
                errors.append(
                    f"Risk 1 fill is '{risk1.get('fill')}', expected '#0D3D1A' (swapped from LOW)"
                )
            if risk3.get("fill") != "#3D1010":
                errors.append(
                    f"Risk 3 fill is '{risk3.get('fill')}', expected '#3D1010' (swapped from HIGH)"
                )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "HIGH and LOW risk card fills swapped correctly"
