import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Board Members label
    bm_label = None
    for label in state.get("labels", []):
        if label["name"] == "Board Members":
            bm_label = label
            break
    if not bm_label:
        return False, "Label 'Board Members' not found."

    # Check gold color
    color = (bm_label.get("color") or "").lower()
    gold_colors = [
        "#ffd700", "#ffb300", "#ffc107", "#ffca28", "#ffd54f",
        "#ffe082", "#f9a825", "#f57f17", "#ff8f00", "#ffa000",
        "#ffab00", "#ffc400", "#ffd600", "gold", "#daa520",
        "#ffb300", "#ff9800", "#ffa726",
    ]
    if color not in gold_colors:
        return False, f"Label color is '{color}', expected a gold color."

    bm_id = bm_label["id"]

    # Q1 Board Meeting (evt_12) external attendees:
    # emily.r@venturelabs.co and lena.j@nordicventures.se
    # (priya.sharma and patrick.oneil are Acme Corp = internal)
    external_senders = {
        "emily.r@venturelabs.co": False,
        "lena.j@nordicventures.se": False,
    }

    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if sender in external_senders:
            if (not e.get("isDone") and not e.get("isTrashed")
                    and not e.get("isSpam") and not e.get("isDraft")
                    and e.get("remindAt") is None):
                if bm_id in e.get("labels", []):
                    external_senders[sender] = True

    missing = [email for email, found in external_senders.items() if not found]
    if missing:
        return False, f"Missing 'Board Members' label on inbox emails from: {', '.join(missing)}"

    return True, "Label 'Board Members' created (gold) and applied to external Board Meeting attendee emails."
