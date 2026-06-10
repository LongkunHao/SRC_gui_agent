# Task: Revoke API key whose label contains a connected provider name, disconnect that provider.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # "Slack Bot Integration" contains "Slack" (a connected provider)
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    if "Slack Bot Integration" in key_labels:
        failures.append("API key 'Slack Bot Integration' should have been revoked")

    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "Slack" in providers:
        failures.append("Slack connected account should have been disconnected")

    if failures:
        return False, "; ".join(failures)
    return True, "Revoked 'Slack Bot Integration' API key and disconnected Slack account."
