import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Tom Bradley has two inbox emails:
    # - id 4: "Re: Infrastructure Migration Plan" (read) → should be archived
    # - id 113: "Database Performance Report - March" (unread) → should be starred
    migration_email = None
    perf_email = None

    for e in state.get("emails", []):
        if e["from"]["email"] == "tom.bradley@acmecorp.com":
            if e["subject"] == "Re: Infrastructure Migration Plan":
                migration_email = e
            elif e["subject"] == "Database Performance Report - March":
                perf_email = e

    if not migration_email:
        return False, "Could not find 'Re: Infrastructure Migration Plan' from Tom Bradley."
    if not perf_email:
        return False, "Could not find 'Database Performance Report - March' from Tom Bradley."

    errors = []
    if not perf_email.get("isStarred", False):
        errors.append("Unread email ('Database Performance Report') is not starred.")
    if not migration_email.get("isDone", False):
        errors.append("Read email ('Infrastructure Migration Plan') is not archived.")

    if errors:
        return False, " ".join(errors)

    return True, "Unread Tom Bradley email starred and read one archived."
