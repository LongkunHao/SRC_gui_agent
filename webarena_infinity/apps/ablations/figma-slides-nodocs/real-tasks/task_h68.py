import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Brand Identity Guidelines: purple bg slides changed to dark navy."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    slides = state.get("slides", [])

    # Brand Identity (pres_002) section-header slides at indices 0,3,5,7,9,12,15
    # originally had backgroundColor #7B61FF, should now be #1a1a2e
    purple_slide_orders = {0, 3, 5, 7, 9, 12, 15}
    pres_slides = [s for s in slides if s.get("presentationId") == "pres_002"]

    if not pres_slides:
        return False, "No slides found for pres_002 (Brand Identity Guidelines)"

    errors = []

    for s in pres_slides:
        order = s.get("order")
        sid = s.get("id")
        bg = s.get("backgroundColor", "")

        if order in purple_slide_orders:
            if bg != "#1a1a2e":
                errors.append(
                    f"{sid} (order {order}): background should be '#1a1a2e', "
                    f"got '{bg}'"
                )

    # Also verify no pres_002 slide still has purple bg
    purple_remaining = [
        s for s in pres_slides
        if s.get("backgroundColor") == "#7B61FF"
    ]
    if purple_remaining:
        ids = [s.get("id") for s in purple_remaining]
        errors.append(f"Slides still with purple background: {ids}")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "7 section-header slides in Brand Identity Guidelines changed "
        "from purple (#7B61FF) to dark navy (#1a1a2e)."
    )
