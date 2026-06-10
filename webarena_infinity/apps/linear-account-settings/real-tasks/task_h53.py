# Task: Revoke OAuth apps with fewer perms than # of connected accounts, disconnect same-domain accounts.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Seed has 5 connected accounts. OAuth apps with <5 perms should be revoked.
    # Raycast(3), Notion(3), Linear Exporter(4), Screenful(4), Marker.io(3) → all revoked
    # Zapier(5) → kept
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    for revoked in ("Raycast", "Notion Integration", "Linear Exporter", "Screenful", "Marker.io"):
        if revoked in app_names:
            failures.append(f"'{revoked}' should have been revoked (fewer than 5 permissions)")
    if "Zapier" not in app_names:
        failures.append("'Zapier' should still be present (has 5 permissions)")

    # Linear email domain: acmecorp.io. Disconnect accounts with same domain.
    # GitHub, GitLab, Slack, Figma all use acmecorp.io → disconnect
    # Google uses gmail.com → keep
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    for disc in ("GitHub", "GitLab", "Slack", "Figma"):
        if disc in providers:
            failures.append(f"'{disc}' should have been disconnected (same email domain)")
    if "Google" not in providers:
        failures.append("'Google' should still be connected (different email domain)")

    if failures:
        return False, "; ".join(failures)
    return True, "OAuth apps with fewer perms revoked; same-domain accounts disconnected."
