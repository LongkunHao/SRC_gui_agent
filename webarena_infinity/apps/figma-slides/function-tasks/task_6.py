import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    total = len(slides)

    matching = [s for s in slides if "Q3 Highlights" in s.get("title", "")]
    titles = [s.get("title", "") for s in matching]

    if len(matching) != 2:
        return False, f"Expected 2 slides with 'Q3 Highlights' in title, found {len(matching)}: {titles}."

    has_original = any(s.get("title") == "Q3 Highlights" for s in matching)
    has_copy = any("(copy)" in s.get("title", "").lower() or "(Copy)" in s.get("title", "") for s in matching)

    if not has_original:
        return False, f"Original 'Q3 Highlights' slide not found. Found: {titles}."
    if not has_copy:
        return False, f"Copy of 'Q3 Highlights' with '(copy)' suffix not found. Found: {titles}."

    if total != 17:
        return False, f"Total slide count is {total}, expected 17."

    return True, "Found original and copy of 'Q3 Highlights' and total slide count is 17."
