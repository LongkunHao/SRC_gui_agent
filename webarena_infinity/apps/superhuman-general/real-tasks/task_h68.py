import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Non-Alex-authored snippets that should be deleted:
    # snip_4 ([Sales] Product Demo, author: Sarah Chen)
    # snip_7 ([HR] Interview Confirmation, author: Rachel Foster)
    # snip_9 ([Engineering] Bug Report Response, author: Nate Patel)
    # snip_11 ([Marketing] Event Invitation, author: Diana Reyes)

    non_alex_names = {
        "[Sales] Product Demo",
        "[HR] Interview Confirmation",
        "[Engineering] Bug Report Response",
        "[Marketing] Event Invitation",
    }

    remaining_non_alex = []
    for s in state.get("snippets", []):
        if s["name"] in non_alex_names:
            remaining_non_alex.append(s["name"])

    if remaining_non_alex:
        return False, f"Non-Alex snippets still exist: {', '.join(remaining_non_alex)}"

    # Check Team Standup snippet exists
    standup = None
    for s in state.get("snippets", []):
        if s["name"] == "Team Standup":
            standup = s
            break

    if not standup:
        return False, "Snippet 'Team Standup' not found."

    expected_body = "Hi team, here are my updates for {date}: {updates}"
    if standup["body"] != expected_body:
        return False, f"Snippet body doesn't match. Got: '{standup['body'][:80]}...'"

    if not standup.get("isShared"):
        return False, "Snippet 'Team Standup' is not shared."

    return True, "Non-Alex snippets deleted and 'Team Standup' created as shared."
