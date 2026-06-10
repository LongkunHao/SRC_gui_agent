import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})

    # Check Pacific timezone
    timezone = settings.get("timezone", "")
    pacific_variants = ["pacific", "los_angeles", "america/los_angeles", "pt", "pst", "pdt", "us/pacific"]
    if not any(v in timezone.lower() for v in pacific_variants):
        return False, f"Timezone is '{timezone}', expected Pacific timezone."

    # Check secondary timezone is disabled/empty
    secondary_tz = settings.get("secondaryTimezone")
    if secondary_tz is not None and secondary_tz != "" and secondary_tz.lower() != "none":
        return False, f"Secondary timezone is '{secondary_tz}', expected none/empty."

    # Check Microsoft Teams meeting link
    meeting_link = settings.get("meetingLink", {})
    provider = meeting_link.get("provider", "")
    provider_lower = provider.lower().replace(" ", "_").replace("-", "_")
    if "teams" not in provider_lower and "microsoft" not in provider_lower:
        return False, f"Meeting link provider is '{provider}', expected Microsoft Teams."

    return True, "Pacific timezone set, no secondary timezone, Microsoft Teams meeting link configured."
