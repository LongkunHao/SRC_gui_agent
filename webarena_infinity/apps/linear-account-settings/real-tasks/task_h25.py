# Task: Disconnect non-SCM connected accounts, unsubscribe from all communication notifications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    accounts = state.get("connectedAccounts", [])
    providers = {a.get("provider") for a in accounts}
    scm_providers = {"GitHub", "GitLab"}

    non_scm_remaining = providers - scm_providers
    if non_scm_remaining:
        failures.append(f"Non-SCM accounts still connected: {non_scm_remaining}")

    missing_scm = scm_providers - providers
    if missing_scm:
        failures.append(f"SCM accounts incorrectly disconnected: {missing_scm}")

    ns = state.get("notificationSettings", {})
    if ns.get("receiveChangelogs"):
        failures.append("receiveChangelogs should be false")
    if ns.get("receiveDpaUpdates"):
        failures.append("receiveDpaUpdates should be false")
    if ns.get("receiveProductUpdates"):
        failures.append("receiveProductUpdates should be false")

    if failures:
        return False, "; ".join(failures)
    return True, "Non-SCM accounts disconnected and all communications unsubscribed."
