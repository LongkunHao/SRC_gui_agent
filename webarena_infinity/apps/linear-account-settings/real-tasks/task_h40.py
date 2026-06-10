# Task: Revoke two most recently authorized OAuth apps, register passkey named after admin workspace.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Most recently authorized: Screenful (2026-01-08), Marker.io (2025-12-15)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Screenful" in app_names:
        failures.append("'Screenful' still present (most recently authorized)")
    if "Marker.io" in app_names:
        failures.append("'Marker.io' still present (second most recently authorized)")

    # Other apps should remain
    for expected in ("Raycast", "Notion Integration", "Zapier", "Linear Exporter"):
        if expected not in app_names:
            failures.append(f"'{expected}' was incorrectly revoked")

    # Admin workspace: Acme Corp → passkey named "Acme Corp"
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "Acme Corp" not in pk_names:
        failures.append(f"Passkey 'Acme Corp' not found. Current passkeys: {pk_names}")

    if failures:
        return False, "; ".join(failures)
    return True, "Two most recently authorized apps revoked and 'Acme Corp' passkey registered."
