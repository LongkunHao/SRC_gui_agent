import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Vendor Review" label
    vr_label = None
    for label in state.get("labels", []):
        if label["name"] == "Vendor Review":
            vr_label = label
            break
    if not vr_label:
        return False, "Label 'Vendor Review' not found."

    # Check color is red-ish
    color = (vr_label.get("color") or "").lower()
    red_colors = ["#f44336", "#e53935", "#d32f2f", "#c62828", "#b71c1c",
                  "#ff1744", "#ff5252", "#ef5350", "#e57373", "#ff0000",
                  "#f44336", "red", "#ff5722", "#e53e3e"]
    if color not in red_colors:
        return False, f"Label color is '{color}', expected a red color."

    vr_id = vr_label["id"]

    # The three vendors flagged in Ben Carter's security assessment:
    # CloudScale (michael.f@cloudscale.dev), MarketingPro (diana.r@marketingpro.co),
    # LogisticsPro (carlos.m@logisticspro.net)
    target_senders = {
        "michael.f@cloudscale.dev": False,
        "diana.r@marketingpro.co": False,
        "carlos.m@logisticspro.net": False,
    }

    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if sender in target_senders:
            if (not e.get("isDone") and not e.get("isTrashed")
                    and not e.get("isSpam") and not e.get("isDraft")
                    and e.get("remindAt") is None):
                if vr_id in e.get("labels", []):
                    target_senders[sender] = True

    missing = [email for email, found in target_senders.items() if not found]
    if missing:
        return False, f"Missing 'Vendor Review' label on inbox emails from: {', '.join(missing)}"

    return True, "Label 'Vendor Review' created (red) and applied to flagged vendor emails."
