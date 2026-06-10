import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find booking page with title "Quick Sync"
    target_bp = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Quick Sync":
            target_bp = bp
            break

    if not target_bp:
        return False, "Could not find booking page titled 'Quick Sync'."

    # Check that isActive is True
    if target_bp.get("isActive") == True:
        return True, "Booking page 'Quick Sync' has been successfully activated."
    else:
        return False, f"Booking page 'Quick Sync' is not active. isActive: {target_bp.get('isActive')}"
