import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Newsletter emails in the Other inbox split (autoLabel == "Newsletter", not done/trashed/spam)
    # In seed data these are: ids 29, 32, 35, 38, 42
    newsletter_subjects = [
        "Today's Briefing: AI Startup Funding Hits Record $12B in Q1",
        "TC Daily: The AI agent wars heat up",
        "Product Hunt Daily Digest - March 6",
        "Morning Brew - Markets surge on Fed pivot signals",
        "HN Weekly: Show HN projects, top stories, and jobs",
    ]

    errors = []
    trashed_count = 0
    for e in state.get("emails", []):
        if e["subject"] in newsletter_subjects:
            if not e.get("isTrashed"):
                errors.append(f"Newsletter '{e['subject'][:50]}...' is not trashed.")
            else:
                trashed_count += 1

    if errors:
        return False, " ".join(errors)

    if trashed_count == 0:
        return False, "No newsletter emails found in trash."

    return True, f"{trashed_count} newsletter emails from the Other split trashed."
