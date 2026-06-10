# Task: Revoke sessions from New York and Seattle, then register a new passkey
# called 'Security Key Backup'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    sessions = state.get("sessions", [])
    failures = []

    ny_sessions = [s for s in sessions if "New York" in s.get("location", "")]
    if ny_sessions:
        names = [s.get("name") for s in ny_sessions]
        failures.append(f"New York session(s) still present: {names}")

    seattle_sessions = [s for s in sessions if "Seattle" in s.get("location", "")]
    if seattle_sessions:
        names = [s.get("name") for s in seattle_sessions]
        failures.append(f"Seattle session(s) still present: {names}")

    passkeys = state.get("passkeys", [])
    passkey_names = [p.get("name") for p in passkeys]
    if "Security Key Backup" not in passkey_names:
        failures.append(f"Passkey 'Security Key Backup' not found. Current passkeys: {passkey_names}")

    if failures:
        return False, "; ".join(failures)
    return True, "New York and Seattle sessions revoked, 'Security Key Backup' passkey registered."
