import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that the Nurses group (ug_3) is included in the Prescription Refill message routing
    for all 5 providers (prov_1 through prov_5)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    message_routing = state.get("messageRouting", {})
    if not message_routing:
        return False, "No messageRouting found in state"

    errors = []
    providers = ["prov_1", "prov_2", "prov_3", "prov_4", "prov_5"]

    for prov_id in providers:
        prov_routing = message_routing.get(prov_id)
        if not prov_routing:
            errors.append(f"No message routing found for {prov_id}")
            continue

        refill_routing = prov_routing.get("Prescription Refill")
        if refill_routing is None:
            errors.append(f"{prov_id} has no 'Prescription Refill' routing category")
            continue

        # refill_routing should be a list of group IDs or objects containing group IDs
        if isinstance(refill_routing, list):
            # Check if ug_3 is in the list (could be strings or objects with id field)
            found = False
            for item in refill_routing:
                if isinstance(item, str) and item == "ug_3":
                    found = True
                    break
                elif isinstance(item, dict) and item.get("id") == "ug_3":
                    found = True
                    break
            if not found:
                errors.append(
                    f"{prov_id} Prescription Refill routing does not include ug_3 (Nurses). "
                    f"Current: {refill_routing}"
                )
        else:
            errors.append(
                f"{prov_id} Prescription Refill routing has unexpected type: {type(refill_routing).__name__}"
            )

    if errors:
        return False, "; ".join(errors)

    return True, "All 5 providers have ug_3 (Nurses) in their Prescription Refill message routing"
