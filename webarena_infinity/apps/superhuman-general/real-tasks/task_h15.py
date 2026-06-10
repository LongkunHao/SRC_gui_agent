import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the Engineering label
    eng_label = None
    for label in state.get("labels", []):
        if label["name"] == "Engineering":
            eng_label = label
            break
    if not eng_label:
        return False, "Label 'Engineering' not found."
    eng_id = eng_label["id"]

    # Check no emails have the Engineering label
    emails_with_eng = []
    for e in state.get("emails", []):
        if eng_id in e.get("labels", []):
            emails_with_eng.append(f"id={e['id']} subject='{e.get('subject', '?')}'")

    if emails_with_eng:
        return False, f"{len(emails_with_eng)} email(s) still have the Engineering label: {'; '.join(emails_with_eng[:5])}{'...' if len(emails_with_eng) > 5 else ''}."

    return True, "Engineering label removed from all emails."
