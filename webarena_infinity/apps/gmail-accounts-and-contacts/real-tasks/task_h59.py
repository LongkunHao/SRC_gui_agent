# Task: Create Inner Circle for starred+Friends, unstar Friends without Work.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contact_labels = state.get("contactLabels", [])
    contacts = state.get("contacts", [])

    # Check Inner Circle label exists with correct color
    inner_label = None
    for lbl in contact_labels:
        if lbl.get("name") == "Inner Circle":
            inner_label = lbl
            break

    if inner_label is None:
        errors.append("Label 'Inner Circle' not found")
    else:
        if inner_label.get("color") != "#E91E63":
            errors.append(
                f"Inner Circle label color is '{inner_label.get('color')}' "
                "instead of '#E91E63'"
            )

    contact_map = {}
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        contact_map[name] = c

    # Marcus Williams (starred + Friends + Work) should have Inner Circle and stay starred
    marcus = contact_map.get("Marcus Williams")
    if marcus and inner_label:
        if inner_label["id"] not in marcus.get("labels", []):
            errors.append("Marcus Williams should have Inner Circle label (starred + Friends)")
        if not marcus.get("isStarred"):
            errors.append("Marcus Williams should remain starred (has Work)")

    # Jake Morrison (starred + Friends, no Work) should have Inner Circle but be unstarred
    jake = contact_map.get("Jake Morrison")
    if jake and inner_label:
        if inner_label["id"] not in jake.get("labels", []):
            errors.append("Jake Morrison should have Inner Circle label (starred + Friends)")
        if jake.get("isStarred"):
            errors.append(
                "Jake Morrison should be unstarred (Friends without Work)"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Inner Circle label created, starred Friends contacts labeled, non-Work Friends unstarred."
