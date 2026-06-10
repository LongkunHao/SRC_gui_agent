import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Emails with "CloudScale" in subject:
    # id 13: "Re: Vendor Agreement - CloudScale"
    # id 21: "CloudScale Contract - Ready to Sign"
    # id 43: "Action Required: CloudScale MSA - Signature Needed"
    # id 101: "CloudScale Migration Checklist"
    cloudscale_subjects = [
        "Re: Vendor Agreement - CloudScale",
        "CloudScale Contract - Ready to Sign",
        "Action Required: CloudScale MSA - Signature Needed",
        "CloudScale Migration Checklist",
    ]

    errors = []
    found = 0
    for e in state.get("emails", []):
        if e["subject"] in cloudscale_subjects:
            found += 1
            if not e.get("isStarred"):
                errors.append(f"'{e['subject']}' is not starred.")

    if found < len(cloudscale_subjects):
        return False, f"Only found {found} of {len(cloudscale_subjects)} CloudScale emails."

    if errors:
        return False, " ".join(errors)

    return True, f"All {found} emails with 'CloudScale' in subject are starred."
