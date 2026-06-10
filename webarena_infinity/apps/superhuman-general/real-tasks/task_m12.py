import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find auto label with name "Design Review"
    target_auto_label = None
    for al in state.get("autoLabels", []):
        if al.get("name") == "Design Review":
            target_auto_label = al
            break

    if not target_auto_label:
        return False, "Could not find an auto label named 'Design Review' in state."

    # Check type is "custom"
    if target_auto_label.get("type") != "custom":
        return False, f"Auto label 'Design Review' has type '{target_auto_label.get('type')}', expected 'custom'."

    # Check criteria contains subject matching "design"
    criteria = target_auto_label.get("criteria", {})
    if isinstance(criteria, dict):
        subject_criteria = criteria.get("subject", "")
        if "design" in str(subject_criteria).lower():
            return True, "Auto label 'Design Review' created as custom type with subject criteria containing 'design'."
        else:
            return False, f"Auto label 'Design Review' criteria does not contain subject with 'design'. Criteria: {criteria}"
    elif isinstance(criteria, list):
        for c in criteria:
            if isinstance(c, dict) and "design" in str(c.get("subject", "")).lower():
                return True, "Auto label 'Design Review' created as custom type with subject criteria containing 'design'."
            if isinstance(c, str) and "design" in c.lower():
                return True, "Auto label 'Design Review' created as custom type with criteria containing 'design'."
        return False, f"Auto label 'Design Review' criteria does not contain 'design'. Criteria: {criteria}"
    elif isinstance(criteria, str):
        if "design" in criteria.lower():
            return True, "Auto label 'Design Review' created as custom type with criteria containing 'design'."
        return False, f"Auto label 'Design Review' criteria does not contain 'design'. Criteria: {criteria}"

    return False, f"Could not parse criteria for auto label 'Design Review'. Criteria: {criteria}"
