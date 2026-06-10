import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify telehealth chat mode changed to 'everyone_in_waiting_room' and
    Amanda Wright (prov_5) has virtual visits activated with correct instructions."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check chat mode
    practice_settings = state.get("practiceSettings", {})
    video_settings = practice_settings.get("videoSettings", {})
    chat_mode = video_settings.get("chatMode")

    if chat_mode != "everyone_in_waiting_room":
        return False, (
            f"practiceSettings.videoSettings.chatMode is '{chat_mode}', "
            f"expected 'everyone_in_waiting_room'"
        )

    # Check Amanda Wright (prov_5) virtual visit settings
    prov_5 = None
    for prov in state.get("providers", []):
        if prov.get("id") == "prov_5":
            prov_5 = prov
            break

    if prov_5 is None:
        return False, "Provider prov_5 (Amanda Wright) not found"

    if not prov_5.get("virtualVisitActivated"):
        return False, (
            f"Amanda Wright (prov_5) does not have virtual visits activated. "
            f"virtualVisitActivated={prov_5.get('virtualVisitActivated')}"
        )

    instructions = prov_5.get("virtualVisitInstructions", "")
    expected_url = "https://meet.bayareafamilymed.com/wright"
    if expected_url not in instructions:
        return False, (
            f"Amanda Wright's virtual visit instructions do not contain expected URL. "
            f"Expected '{expected_url}' in instructions. Got: {instructions!r}"
        )

    return True, (
        "Chat mode set to 'everyone_in_waiting_room' and Amanda Wright has "
        "virtual visits activated with correct instructions"
    )
