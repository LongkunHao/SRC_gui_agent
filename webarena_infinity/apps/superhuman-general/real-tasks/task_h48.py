import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    snippets = state.get("snippets", [])
    snippet_map = {s["name"]: s for s in snippets}
    errors = []

    # Shared snippets that should have been unshared (open rate < 80%):
    # snip_4 [Sales] Product Demo (76%), snip_9 [Engineering] Bug Report Response (71%),
    # snip_11 [Marketing] Event Invitation (68%)
    should_unshare = ["[Sales] Product Demo", "[Engineering] Bug Report Response",
                      "[Marketing] Event Invitation"]
    for name in should_unshare:
        snip = snippet_map.get(name)
        if snip and snip.get("isShared"):
            errors.append(f"'{name}' is still shared (open rate < 80%, should be unshared).")

    # Unshared snippets that should have been deleted (< 20 sends):
    # snip_6 Out of Office (18 sends), snip_12 Decline Politely (15 sends)
    should_delete = ["Out of Office", "Decline Politely"]
    for name in should_delete:
        if name in snippet_map:
            errors.append(f"'{name}' still exists (< 20 sends, should be deleted).")

    # Snippets that should remain shared (open rate >= 80%):
    should_stay_shared = ["Meeting Follow-up", "Introduction",
                          "[Sales] Proposal Follow-up", "[HR] Interview Confirmation"]
    for name in should_stay_shared:
        snip = snippet_map.get(name)
        if snip and not snip.get("isShared"):
            errors.append(f"'{name}' was incorrectly unshared (open rate >= 80%).")

    if errors:
        return False, " ".join(errors)

    return True, "Shared snippets with low open rate unshared; unshared snippets with low sends deleted."
