import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # rep_002 is the active repeating invoice that saves as draft (CloudNine)
    ri = next((r for r in state.get("repeatingInvoices", []) if r.get("id") == "rep_002"), None)
    if ri is None:
        return False, "Repeating invoice rep_002 not found."

    # Should now have Bright Spark Electrical as contact
    bright_spark = next((c for c in state.get("contacts", []) if "Bright Spark" in c.get("name", "")), None)
    if bright_spark is None:
        return False, "Bright Spark Electrical contact not found."

    if ri.get("contactId") != bright_spark.get("id"):
        actual_contact = next(
            (c for c in state.get("contacts", []) if c.get("id") == ri.get("contactId")), None
        )
        actual_name = actual_contact.get("name") if actual_contact else ri.get("contactId")
        return False, f"rep_002 contact should be Bright Spark Electrical, got '{actual_name}'."

    return True, "rep_002 (active, saves as draft) contact changed to Bright Spark Electrical."
