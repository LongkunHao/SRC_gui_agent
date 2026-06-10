import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify All Providers in MRR routing for all providers + North Beach Office location."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check All Providers (ug_4) in Medical Records Request for all providers
    routing = state.get("messageRouting", {})
    provider_ids = [p.get("id") for p in state.get("providers", [])]

    missing = []
    for pid in provider_ids:
        prov_routing = routing.get(pid, {})
        mrr = prov_routing.get("Medical Records Request", [])
        if "ug_4" not in mrr:
            missing.append(pid)

    if missing:
        return False, (
            f"All Providers (ug_4) missing from Medical Records Request routing for: "
            f"{', '.join(missing)}"
        )

    # Check North Beach Office location
    locations = state.get("practiceSettings", {}).get("practiceLocations", [])
    nb_found = False
    for loc in locations:
        if loc.get("name") == "North Beach Office":
            nb_found = True
            if "2200 Mason" not in loc.get("address", ""):
                return False, f"North Beach Office has wrong address: {loc.get('address')}"
            if loc.get("posCode") != "11":
                return False, f"North Beach Office has POS code '{loc.get('posCode')}', expected '11'"
            break

    if not nb_found:
        return False, "North Beach Office location not found"

    return True, "All Providers added to MRR routing for all providers and North Beach Office created"
