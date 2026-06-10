import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Ben Carter's security assessment (email 83) flagged:
    # CloudScale (cloudscale.dev), MarketingPro (marketingpro.co), LogisticsPro (logisticspro.net)

    al = None
    for auto_label in state.get("autoLabels", []):
        if auto_label.get("name") == "Security Risk":
            al = auto_label
            break

    if not al:
        return False, "Auto label 'Security Risk' not found."

    if al.get("type") != "custom":
        return False, f"Auto label type is '{al.get('type')}', expected 'custom'."

    criteria = al.get("criteria", {})
    from_criteria = (criteria.get("from") or "").lower()

    required_domains = ["cloudscale.dev", "marketingpro.co", "logisticspro.net"]
    missing = [d for d in required_domains if d not in from_criteria]
    if missing:
        return False, f"Auto label 'from' criteria missing domains: {', '.join(missing)}. Got: '{criteria.get('from')}'"

    return True, "Auto label 'Security Risk' created with all three vendor domains."
