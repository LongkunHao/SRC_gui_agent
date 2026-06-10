import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Spam emails by id: 75 (Prince Okafor), 76 (CryptoGains), 77 (Discount Pharma)
    spam_ids = [75, 76, 77]
    spam_subjects = {
        75: "URGENT: Inheritance Notification",
        76: "Make $50K/day",
        77: "Limited Time: 90% Off",
    }

    emails_by_id = {}
    for e in state.get("emails", []):
        emails_by_id[e["id"]] = e

    not_trashed = []
    for sid in spam_ids:
        email = emails_by_id.get(sid)
        if not email:
            # Email might have been fully deleted; that's acceptable
            continue
        if not email.get("isTrashed", False):
            not_trashed.append(f"id={sid} subject='{spam_subjects.get(sid, '?')}'")

    if not_trashed:
        return False, f"The following spam emails are not trashed: {'; '.join(not_trashed)}."

    return True, "All three spam emails have been moved to trash."
