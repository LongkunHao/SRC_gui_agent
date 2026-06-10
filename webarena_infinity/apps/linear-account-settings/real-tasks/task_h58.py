# Task: Remove earliest passkey, revoke earliest OAuth, disconnect most recent connected account.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Earliest created passkey: MacBook Pro Touch ID (2025-08-15)
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "MacBook Pro Touch ID" in pk_names:
        failures.append("'MacBook Pro Touch ID' should have been removed (earliest created)")

    # Earliest authorized OAuth: Zapier (2025-05-20)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Zapier" in app_names:
        failures.append("'Zapier' should have been revoked (earliest authorized)")

    # Most recently connected account: Figma (2025-01-12)
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "Figma" in providers:
        failures.append("'Figma' should have been disconnected (most recently connected)")

    if failures:
        return False, "; ".join(failures)
    return True, "Earliest passkey removed, earliest OAuth revoked, newest connected account disconnected."
