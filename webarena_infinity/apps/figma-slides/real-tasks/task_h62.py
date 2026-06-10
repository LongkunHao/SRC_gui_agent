import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # In seed data, alignment survey responses:
    # user_002 (Marcus): 4, user_003 (Aiko): 3, user_005 (Priya): 2,
    # user_007 (Elena): 4, user_008 (David): 5
    # Score <= 3: Aiko (user_003) and Priya (user_005) -> Viewer
    low_confidence_ids = {"user_003", "user_005"}

    for c in state.get("collaborators", []):
        if c.get("id") in low_confidence_ids:
            if c.get("role") != "Viewer":
                errors.append(
                    f"{c.get('name')} role is '{c.get('role')}', expected 'Viewer' "
                    f"(low confidence score)"
                )

    # Check that both interactions have results hidden
    for s in state.get("slides", []):
        if s.get("title") == "Team Survey Results":
            for obj in s.get("objects", []):
                if obj.get("type") == "liveInteraction":
                    if obj.get("hideResults") is not True:
                        itype = obj.get("interactionType", obj.get("name", "unknown"))
                        errors.append(
                            f"{itype} hideResults is {obj.get('hideResults')}, expected True"
                        )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Low-confidence collaborators set to Viewer; interaction results hidden"
