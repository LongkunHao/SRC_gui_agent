import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "External Partners" label
    ep_label = None
    for label in state.get("labels", []):
        if label["name"] == "External Partners":
            ep_label = label
            break
    if not ep_label:
        return False, "Label 'External Partners' not found."
    if ep_label.get("type") != "user":
        return False, f"Label type is '{ep_label.get('type')}', expected 'user'."

    # Check color is orange-ish
    color = (ep_label.get("color") or "").lower()
    orange_colors = ["#ff9800", "#ff8c00", "#f57c00", "#fb8c00", "#ef6c00", "#e65100", "#ffa500", "orange"]
    if color not in orange_colors:
        return False, f"Label color is '{color}', expected an orange color."

    ep_id = ep_label["id"]

    # Check inbox emails from DesignHub, FinancePlus, CloudScale have the label
    target_emails = {
        "marcus.w@designhub.io": False,
        "david.kim@financeplus.com": False,
        "michael.f@cloudscale.dev": False,
    }

    for e in state.get("emails", []):
        sender = e.get("from", {}).get("email", "")
        if sender in target_emails:
            # Only check inbox emails (not done, not trashed, not spam, not draft)
            if (not e.get("isDone") and not e.get("isTrashed") and not e.get("isSpam")
                    and not e.get("isDraft") and e.get("remindAt") is None):
                if ep_id in e.get("labels", []):
                    target_emails[sender] = True

    missing = [email for email, found in target_emails.items() if not found]
    if missing:
        return False, f"Missing 'External Partners' label on inbox emails from: {', '.join(missing)}"

    return True, "Label 'External Partners' created with orange color and applied to DesignHub, FinancePlus, and CloudScale inbox emails."
