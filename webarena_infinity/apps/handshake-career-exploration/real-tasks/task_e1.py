"""
Task: Follow Spotify on Handshake.
Verify: emp_13 is in currentUser.followedEmployerIds AND emp_13 followCount > 19800.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])

    if "emp_13" not in followed:
        return False, (
            f"Spotify (emp_13) is not in currentUser.followedEmployerIds. "
            f"Currently following: {followed}"
        )

    employers = state.get("employers", [])
    spotify = next((e for e in employers if e.get("id") == "emp_13"), None)
    if spotify is None:
        return False, "Employer emp_13 (Spotify) not found in employers list."

    follow_count = spotify.get("followCount", 0)
    if follow_count <= 19800:
        return False, (
            f"Spotify (emp_13) followCount is {follow_count}, expected > 19800. "
            f"The follow action may not have incremented the count."
        )

    return True, (
        f"Spotify (emp_13) is followed. followCount={follow_count}."
    )
