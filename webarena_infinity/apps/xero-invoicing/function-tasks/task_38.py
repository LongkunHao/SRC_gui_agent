import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    theme = next((t for t in state["brandingThemes"] if t["name"] == "Modern Minimalist"), None)
    if not theme:
        return False, "Branding theme 'Modern Minimalist' not found."

    if theme.get("isDefault"):
        return False, "New theme should not be the default."

    if theme["paymentTerms"] != "Net 14 days":
        return False, f"Payment terms are '{theme['paymentTerms']}', expected 'Net 14 days'."

    if theme["showTaxNumber"] is not True:
        return False, "showTaxNumber should be True."

    if theme["showPaymentAdvice"] is not True:
        return False, "showPaymentAdvice should be True."

    return True, "Branding theme 'Modern Minimalist' created successfully."
