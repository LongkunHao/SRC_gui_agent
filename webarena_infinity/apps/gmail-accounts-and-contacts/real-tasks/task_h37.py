# Task: Move Alex Rivera to main contacts, set company/title, add Work label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    other_contacts = state.get("otherContacts", [])

    # Alex Rivera should be in main contacts
    alex = None
    for c in contacts:
        if c.get("email") == "alex.rivera@notion.so":
            alex = c
            break

    if alex is None:
        errors.append("Alex Rivera (alex.rivera@notion.so) not found in main contacts")
    else:
        if alex.get("company") != "Notion":
            errors.append(
                f"Alex Rivera's company is '{alex.get('company')}' instead of 'Notion'"
            )
        if alex.get("jobTitle") != "Product Manager":
            errors.append(
                f"Alex Rivera's job title is '{alex.get('jobTitle')}' "
                "instead of 'Product Manager'"
            )
        if "clabel_3" not in alex.get("labels", []):
            errors.append("Alex Rivera does not have the Work label")

    # Should not be in other contacts anymore
    in_other = any(
        c.get("email") == "alex.rivera@notion.so" for c in other_contacts
    )
    if in_other:
        errors.append("Alex Rivera still in other contacts after move")

    if errors:
        return False, "; ".join(errors)
    return True, "Alex Rivera moved, company set to Notion, title to Product Manager, Work label added."
