import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check for auto label "Partner"
    partner_al = None
    for al in state.get("autoLabels", []):
        if al.get("name") == "Partner":
            partner_al = al
            break
    if not partner_al:
        return False, "Auto label 'Partner' not found."
    if not partner_al.get("enabled"):
        return False, "Auto label 'Partner' is not enabled."
    if partner_al.get("type") != "custom":
        return False, f"Auto label 'Partner' type is '{partner_al.get('type')}', expected 'custom'."

    # Check criteria references the three domains
    criteria = partner_al.get("criteria", {})
    from_criteria = str(criteria.get("from", "")).lower()
    domains = ["designhub.io", "financeplus.com", "cloudscale.dev"]
    missing_domains = [d for d in domains if d not in from_criteria]
    if missing_domains:
        return False, f"Auto label criteria missing domains: {', '.join(missing_domains)}. Got: {from_criteria}"

    # Check for split "Partners"
    partner_split = None
    for s in state.get("splits", []):
        if s.get("name") == "Partners":
            partner_split = s
            break
    if not partner_split:
        return False, "Inbox split 'Partners' not found."

    # Check the split references the Partner auto label
    split_criteria = partner_split.get("criteria", {})
    auto_label_ref = str(split_criteria.get("autoLabel", "")).lower()
    if "partner" not in auto_label_ref:
        return False, f"Split criteria autoLabel is '{auto_label_ref}', expected to reference 'Partner'."

    return True, "Auto label 'Partner' and inbox split 'Partners' created successfully."
