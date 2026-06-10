import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Offline Editors in seed data:
    # - Priya Sharma (user_005): comment is already resolved → no change
    # - Elena Kowalski (user_007): has unresolved comment → resolve + role to Viewer
    #
    # James O'Brien (user_004) is offline but Viewer, not Editor → excluded

    # Elena's comment should be resolved
    for c in state.get("comments", []):
        if c.get("userId") == "user_007":
            if c.get("resolved") is not True:
                errors.append("Elena Kowalski's comment should be resolved")

    # Elena's role should be Viewer
    for collab in state.get("collaborators", []):
        if collab.get("name") == "Elena Kowalski":
            if collab.get("role") != "Viewer":
                errors.append(
                    f"Elena Kowalski's role is '{collab.get('role')}', expected 'Viewer'"
                )
            break

    # Priya should NOT have her role changed (her comment was already resolved)
    for collab in state.get("collaborators", []):
        if collab.get("name") == "Priya Sharma":
            if collab.get("role") != "Editor":
                errors.append(
                    f"Priya Sharma's role should remain 'Editor' "
                    f"(her comment was already resolved), got '{collab.get('role')}'"
                )
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Elena: comment resolved, role→Viewer; Priya: unchanged (comment was resolved)"
