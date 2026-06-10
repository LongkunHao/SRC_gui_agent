# Task: Revoke OAuth app with most permissions, remove most recently registered passkey.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Zapier has 5 permissions (the most)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Zapier" in app_names:
        failures.append("'Zapier' still present (has most permissions)")

    # iPhone Face ID was created most recently (2025-11-10)
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "iPhone Face ID" in pk_names:
        failures.append("'iPhone Face ID' still present (most recently registered)")

    if failures:
        return False, "; ".join(failures)
    return True, "OAuth app with most permissions revoked and newest passkey removed."
