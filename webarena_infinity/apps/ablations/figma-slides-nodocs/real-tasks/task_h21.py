import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Set the share visibility to public on the presentation with the most slides."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    if not presentations:
        return False, "No presentations found in state."

    # pres_013 (Mobile Design System Components) has 25 slides — the most
    most_slides_pres = max(presentations, key=lambda p: p.get("slideCount", 0))
    expected_id = "pres_013"

    if most_slides_pres.get("id") != expected_id:
        return False, (
            f"Expected pres_013 to have the most slides, but found "
            f"{most_slides_pres.get('id')} ({most_slides_pres.get('title')}) "
            f"with {most_slides_pres.get('slideCount')} slides."
        )

    pres_map = {p["id"]: p for p in presentations}
    if expected_id not in pres_map:
        return False, "pres_013 (Mobile Design System Components) not found."

    p = pres_map[expected_id]
    vis = p.get("shareSettings", {}).get("visibility")
    if vis != "public":
        return False, (
            f"Expected pres_013 visibility=='public', got visibility=='{vis}'."
        )

    return True, "Presentation with most slides (pres_013, 25 slides) has public visibility."
