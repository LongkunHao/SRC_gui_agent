"""Verify: Copy highest-numbered paid Ironclad invoice (INV-0091), change contact to Heritage Craft, approve."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    errors = []

    # Heritage Craft Brewery = con_20
    # Find new invoice for con_20 that wasn't in seed data
    con_20_invoices = [i for i in invoices if i.get("contactId") == "con_20"]
    # Seed invoices for con_20: inv_20, inv_45, inv_70, inv_95
    seed_ids = {"inv_20", "inv_45", "inv_70", "inv_95"}
    new_invoices = [i for i in con_20_invoices if i["id"] not in seed_ids]

    if not new_invoices:
        return False, "No new invoice found for Heritage Craft Brewery (con_20)"

    inv = new_invoices[0]

    # Should be approved (awaiting_payment)
    if inv.get("status") != "awaiting_payment":
        errors.append(f"Copy status is '{inv.get('status')}', expected 'awaiting_payment'")

    # Should have same line items as inv_91 (3 line items)
    lis = inv.get("lineItems", [])
    if len(lis) < 3:
        errors.append(f"Expected at least 3 line items (copied from INV-0091), found {len(lis)}")

    # Check line items match inv_91 content
    legal = next((l for l in lis if "legal" in (l.get("description") or "").lower()), None)
    contract = next((l for l in lis if "contract" in (l.get("description") or "").lower()), None)
    compliance = next((l for l in lis if "compliance" in (l.get("description") or "").lower()), None)

    if not legal:
        errors.append("No 'Legal document review' line item found")
    if not contract:
        errors.append("No 'Contract drafting services' line item found")
    if not compliance:
        errors.append("No 'Compliance advisory' line item found")

    if errors:
        return False, "; ".join(errors)
    return True, "INV-0091 copied to Heritage Craft Brewery and approved"
