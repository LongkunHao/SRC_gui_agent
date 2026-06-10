import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Product Demo":
            if bp.get("isActive") is False:
                return True, "The Product Demo booking page is deactivated."
            return False, f"The Product Demo booking page is still active (isActive={bp.get('isActive')!r})."

    return False, "Could not find the Product Demo booking page."
