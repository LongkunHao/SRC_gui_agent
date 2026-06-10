import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    snippets = state.get("snippets", [])

    # 1. Check "Contract Follow-up" exists and is shared
    contract_snip = None
    for s in snippets:
        if s["name"] == "Contract Follow-up":
            contract_snip = s
            break
    if not contract_snip:
        return False, "Snippet 'Contract Follow-up' not found."
    if not contract_snip.get("isShared"):
        return False, "Snippet 'Contract Follow-up' exists but is not shared."

    expected_body = "Hi {first_name}, please sign the {contract_name} contract by {deadline}. Thanks, Alex"
    if contract_snip.get("body", "").strip() != expected_body:
        return False, f"Snippet body does not match. Got: '{contract_snip.get('body')}'"

    # 2. Check "Scheduling Request" is deleted
    for s in snippets:
        if s["name"] == "Scheduling Request":
            return False, "Snippet 'Scheduling Request' should have been deleted but still exists."

    # 3. Check "[Sales] Product Demo" is not shared
    demo_snip = None
    for s in snippets:
        if s["name"] == "[Sales] Product Demo":
            demo_snip = s
            break
    if not demo_snip:
        return False, "Snippet '[Sales] Product Demo' not found (should still exist, just unshared)."
    if demo_snip.get("isShared"):
        return False, "Snippet '[Sales] Product Demo' is still shared; it should be unshared."

    return True, "Contract Follow-up created and shared, Scheduling Request deleted, [Sales] Product Demo unshared."
