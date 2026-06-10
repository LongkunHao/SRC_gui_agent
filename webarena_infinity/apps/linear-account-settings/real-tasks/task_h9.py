# Task: Create API key 'GitHub Actions' and revoke the 'CI/CD Pipeline' key.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]

    if "CI/CD Pipeline" in labels:
        return False, "'CI/CD Pipeline' key still exists"
    if "GitHub Actions" not in labels:
        return False, "'GitHub Actions' key not found"
    return True, "API key 'GitHub Actions' created and 'CI/CD Pipeline' revoked."
