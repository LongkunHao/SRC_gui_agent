import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Most recent non-Acme reader in Recent Opens: Emily Rodriguez (emily.r@venturelabs.co)
    # She opened email 69 at 2026-03-07T08:30:00Z

    # Find a forwarded email to Emily about the roadmap
    found = None
    for e in state.get("emails", []):
        if e["from"]["email"] == "alex.morgan@acmecorp.com" and not e.get("isDraft"):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "emily.r@venturelabs.co" in to_emails:
                subj = e.get("subject", "").lower()
                if "roadmap" in subj and ("fwd" in subj or "forward" in subj):
                    found = e
                    break

    if not found:
        return False, "No forwarded roadmap email found addressed to Emily Rodriguez."

    return True, "Roadmap email forwarded to Emily Rodriguez (most recent external reader in Recent Opens)."
