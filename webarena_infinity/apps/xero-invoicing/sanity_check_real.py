#!/usr/bin/env python3
"""
Sanity check for xero-invoicing real tasks.

For each task: reset → apply solve (state mutation) → verify → assert pass.
Validates that verifiers correctly recognize solved tasks.
"""

import argparse
import importlib.util
import json
import os
import signal
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy

import requests

APP_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(APP_DIR, "real-tasks.json")
DATA_JS = os.path.join(APP_DIR, "js", "data.js")
SERVER_PY = os.path.join(APP_DIR, "server.py")

# ---------------------------------------------------------------------------
# Seed state generation
# ---------------------------------------------------------------------------

_SEED_STATE_JS = r"""
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

const state = {
    _seedVersion: SEED_DATA_VERSION,
    contacts: JSON.parse(JSON.stringify(CONTACTS)),
    invoices: JSON.parse(JSON.stringify(INVOICES)),
    quotes: JSON.parse(JSON.stringify(QUOTES)),
    creditNotes: JSON.parse(JSON.stringify(CREDIT_NOTES)),
    repeatingInvoices: JSON.parse(JSON.stringify(REPEATING_INVOICES)),
    items: JSON.parse(JSON.stringify(ITEMS)),
    taxRates: JSON.parse(JSON.stringify(TAX_RATES)),
    accounts: JSON.parse(JSON.stringify(ACCOUNTS)),
    trackingCategories: JSON.parse(JSON.stringify(TRACKING_CATEGORIES)),
    currencies: JSON.parse(JSON.stringify(CURRENCIES)),
    brandingThemes: JSON.parse(JSON.stringify(BRANDING_THEMES)),
    invoiceSettings: JSON.parse(JSON.stringify(INVOICE_SETTINGS)),
    invoiceReminders: JSON.parse(JSON.stringify(INVOICE_REMINDERS)),
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    _nextInvoiceNum: INVOICE_SETTINGS.invoiceNextNumber,
    _nextQuoteNum: INVOICE_SETTINGS.quoteNextNumber,
    _nextCreditNoteNum: INVOICE_SETTINGS.creditNoteNextNumber,
    _nextContactId: 26,
    _nextItemId: 16,
    _nextReminderId: 5,
    _nextRepeatId: 6,
    _nextLineItemId: 1000,
    _nextPaymentId: 100,
    _nextThemeId: 5,
};
process.stdout.write(JSON.stringify(state));
"""


def generate_seed_state() -> dict:
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, DATA_JS],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Seed state generation failed:\n{result.stderr}")
    return json.loads(result.stdout)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_entity(entities, **kwargs):
    for e in entities:
        if all(e.get(k) == v for k, v in kwargs.items()):
            return e
    raise ValueError(f"Entity not found: {kwargs}")


def find_invoice(state, number):
    return find_entity(state["invoices"], number=number)


def find_quote(state, number):
    return find_entity(state["quotes"], number=number)


def find_credit_note(state, number):
    return find_entity(state["creditNotes"], number=number)


def find_contact(state, name):
    return find_entity(state["contacts"], name=name)


def find_reminder(state, timing, days):
    return find_entity(state["invoiceReminders"], timing=timing, days=days)


def find_theme(state, id):
    return find_entity(state["brandingThemes"], id=id)


def find_repeating(state, id):
    return find_entity(state["repeatingInvoices"], id=id)


# ---------------------------------------------------------------------------
# Solve functions — one per task, derived from verifiers
# ---------------------------------------------------------------------------

# ===== EASY =====

def solve_task_e1(state):
    """Approve Murray River Winery draft invoice INV-0058."""
    inv = find_invoice(state, "INV-0058")
    inv["status"] = "awaiting_payment"


def solve_task_e2(state):
    """Void Sapphire Bay Resort invoice INV-0054."""
    inv = find_invoice(state, "INV-0054")
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_e3(state):
    """Delete Bright Spark Electrical draft invoice INV-0059."""
    inv = find_invoice(state, "INV-0059")
    inv["status"] = "deleted"


def solve_task_e4(state):
    """Mark Stellar Education invoice INV-0057 as sent."""
    inv = find_invoice(state, "INV-0057")
    inv["status"] = "awaiting_payment"
    inv["sentAt"] = "2026-03-06T12:00:00Z"


def solve_task_e5(state):
    """Accept Redback Mining Supplies quote QU-0023."""
    quo = find_quote(state, "QU-0023")
    quo["status"] = "accepted"


def solve_task_e6(state):
    """Decline Metro Fabrication Works quote QU-0028."""
    quo = find_quote(state, "QU-0028")
    quo["status"] = "declined"


def solve_task_e7(state):
    """Delete Horizon Media declined quote QU-0026."""
    quo = find_quote(state, "QU-0026")
    quo["status"] = "deleted"


def solve_task_e8(state):
    """Approve Pacific Freight Lines draft credit note CN-0011."""
    cn = find_credit_note(state, "CN-0011")
    cn["status"] = "awaiting_payment"


def solve_task_e9(state):
    """Set Professional Services as default branding theme."""
    for t in state["brandingThemes"]:
        t["isDefault"] = (t["id"] == "theme_professional")


def solve_task_e10(state):
    """Delete Simple Clean branding theme."""
    state["brandingThemes"] = [t for t in state["brandingThemes"] if t["id"] != "theme_simple"]


def solve_task_e11(state):
    """Turn off tax number display on Standard theme."""
    theme = find_theme(state, "theme_standard")
    theme["showTaxNumber"] = False


def solve_task_e12(state):
    """Disable 7-day advance reminder."""
    rem = find_reminder(state, "before", 7)
    rem["enabled"] = False


def solve_task_e13(state):
    """Enable 30-day overdue reminder."""
    rem = find_reminder(state, "after", 30)
    rem["enabled"] = True


def solve_task_e14(state):
    """Switch default tax mode to inclusive."""
    state["invoiceSettings"]["defaultTaxMode"] = "inclusive"


def solve_task_e15(state):
    """Hide discount column."""
    state["invoiceSettings"]["showDiscountColumn"] = False


def solve_task_e16(state):
    """Change invoice prefix to TAX-."""
    state["invoiceSettings"]["invoicePrefix"] = "TAX-"


def solve_task_e17(state):
    """Change default payment terms to end of following month."""
    state["invoiceSettings"]["defaultDueDate"] = {"type": "endOfFollowingMonth", "days": 0}


def solve_task_e18(state):
    """Submit Redback Mining draft invoice INV-0060 for approval."""
    inv = find_invoice(state, "INV-0060")
    inv["status"] = "awaiting_approval"


def solve_task_e19(state):
    """Delete Summit Health draft repeating invoice rep_005."""
    state["repeatingInvoices"] = [r for r in state["repeatingInvoices"] if r["id"] != "rep_005"]


def solve_task_e20(state):
    """Hide item code column."""
    state["invoiceSettings"]["showItemCode"] = False


# ===== MEDIUM =====

def solve_task_m1(state):
    """Record full payment for Vanguard Security hosting invoice INV-0053."""
    inv = find_invoice(state, "INV-0053")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 823.90,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 823.90
    inv["amountDue"] = 0
    inv["status"] = "paid"


def solve_task_m2(state):
    """Copy Baxter & Associates invoice INV-0046 to new draft."""
    src = find_invoice(state, "INV-0046")
    copy = deepcopy(src)
    num = state["_nextInvoiceNum"]
    copy["id"] = f"inv_{num:03d}"
    copy["number"] = state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}"
    state["_nextInvoiceNum"] = num + 1
    copy["status"] = "draft"
    copy["payments"] = []
    copy["amountPaid"] = 0
    copy["amountDue"] = copy["total"]
    copy["sentAt"] = None
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_m3(state):
    """Pay off Pinnacle Construction INV-0045."""
    inv = find_invoice(state, "INV-0045")
    remaining = inv["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": remaining,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += remaining
    inv["amountDue"] = 0
    inv["status"] = "paid"


def solve_task_m4(state):
    """Create new invoice for Atlas Engineering for 20 hours dev work."""
    contact = find_contact(state, "Atlas Engineering Consultants")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 20 * 185.00
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_001",
            "description": "Software Development - Hourly Rate",
            "quantity": 20,
            "unitPrice": 185.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_m5(state):
    """Change CloudNine repeating invoice frequency to quarterly."""
    ri = find_repeating(state, "rep_002")
    ri["frequency"] = "quarterly"


def solve_task_m6(state):
    """Create branding theme 'Corporate Executive'."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Corporate Executive",
        "isDefault": False,
        "logoUrl": "",
        "paymentTerms": "Net 14 days",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": True,
    }
    state["brandingThemes"].append(theme)


def solve_task_m7(state):
    """Update INV-0058 reference to MRW-MARCH-2026."""
    inv = find_invoice(state, "INV-0058")
    inv["reference"] = "MRW-MARCH-2026"


def solve_task_m8(state):
    """Allocate CN-0009 ($249.75) to INV-0049."""
    cn = find_credit_note(state, "CN-0009")
    inv = find_invoice(state, "INV-0049")
    amount = 249.75
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += amount
    inv["amountDue"] -= amount
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_m9(state):
    """Create new quote for Sapphire Bay Resort for 5 days training."""
    contact = find_contact(state, "Sapphire Bay Resort")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 5 * 2200.00
    tax = subtotal * 0.10
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_006",
            "description": "On-site Training - Per Day",
            "quantity": 5,
            "unitPrice": 2200.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_m10(state):
    """Send Fresh Start Catering draft quote QU-0025."""
    quo = find_quote(state, "QU-0025")
    quo["status"] = "sent"
    quo["sentAt"] = "2026-03-06T12:00:00Z"


def solve_task_m11(state):
    """Create reminder for 21 days after due date."""
    rid = state["_nextReminderId"]
    state["_nextReminderId"] = rid + 1
    rem = {
        "id": f"rem_{rid:03d}",
        "enabled": True,
        "timing": "after",
        "days": 21,
        "subject": "Third reminder: Invoice overdue - {InvoiceNumber}",
        "body": "Dear {ContactName}, Invoice {InvoiceNumber} is now 21 days past due.",
        "includeInvoicePdf": True,
        "includeSummary": True,
    }
    state["invoiceReminders"].append(rem)


def solve_task_m12(state):
    """Delete 14-day overdue reminder."""
    state["invoiceReminders"] = [
        r for r in state["invoiceReminders"]
        if not (r["timing"] == "after" and r["days"] == 14)
    ]


def solve_task_m13(state):
    """Set end date of December 2026 on Greenfield Organics repeating invoice."""
    ri = find_repeating(state, "rep_001")
    ri["endDate"] = "2026-12-31"


def solve_task_m14(state):
    """Remove partial payment from Pinnacle Construction INV-0045."""
    inv = find_invoice(state, "INV-0045")
    inv["payments"] = []
    inv["amountPaid"] = 0
    inv["amountDue"] = inv["total"]
    if inv["status"] == "paid":
        inv["status"] = "awaiting_payment"


def solve_task_m15(state):
    """Copy Fresh Start Catering quote QU-0025 to new draft."""
    src = find_quote(state, "QU-0025")
    copy = deepcopy(src)
    num = state["_nextQuoteNum"]
    copy["id"] = f"quo_{num:03d}"
    copy["number"] = state["invoiceSettings"]["quotePrefix"] + f"{num:04d}"
    state["_nextQuoteNum"] = num + 1
    copy["status"] = "draft"
    copy["sentAt"] = None
    copy["isInvoiced"] = False
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["quotes"].append(copy)


def solve_task_m16(state):
    """Rename Retail theme to 'Retail Premium'."""
    theme = find_theme(state, "theme_retail")
    theme["name"] = "Retail Premium"


def solve_task_m17(state):
    """Create credit note for Greenfield Organics for $200 hosting credit."""
    contact = find_contact(state, "Greenfield Organics")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 200.00
    tax = 20.00
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": None,
            "description": "Hosting credit",
            "quantity": 1,
            "unitPrice": 200.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_m18(state):
    """Change credit note prefix to CR-."""
    state["invoiceSettings"]["creditNotePrefix"] = "CR-"


def solve_task_m19(state):
    """Update Cascade Software repeating invoice reference."""
    ri = find_repeating(state, "rep_003")
    ri["reference"] = "CSS-LIC-MONTHLY"


def solve_task_m20(state):
    """Add title to Horizon Media invoice INV-0056."""
    inv = find_invoice(state, "INV-0056")
    inv["title"] = "Q1 Digital Campaign Work"


# ===== HARD =====

def solve_task_h1(state):
    """Create invoice from accepted Pinnacle Construction quote QU-0022."""
    quo = find_quote(state, "QU-0022")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    line_items = deepcopy(quo["lineItems"])
    for li in line_items:
        li["id"] = f"li_{lid}"
        lid += 1
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": quo["contactId"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": quo["reference"],
        "currency": quo["currency"],
        "brandingThemeId": quo["brandingThemeId"],
        "taxMode": quo["taxMode"],
        "lineItems": line_items,
        "subtotal": quo["subtotal"],
        "taxTotal": quo["taxTotal"],
        "total": quo["total"],
        "amountDue": quo["total"],
        "amountPaid": 0,
        "payments": [],
        "notes": [
            {"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-06T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_h2(state):
    """Create invoice for Wellington & Partners in NZD for 16 hours consulting, send it."""
    contact = find_contact(state, "Wellington & Partners Accounting")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 16 * 250.00
    tax = 0
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "NZD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_002",
            "description": "Consulting Services - Per Hour",
            "quantity": 16,
            "unitPrice": 250.00,
            "discountPercent": 0,
            "accountId": "acc_260",
            "taxRateId": "tax_gst_free",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": "2026-03-06T12:00:00Z",
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h3(state):
    """Allocate CloudNine credit note CN-0012 to INV-0047."""
    cn = find_credit_note(state, "CN-0012")
    inv = find_invoice(state, "INV-0047")
    amount = 2035.00
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += amount
    inv["amountDue"] -= amount
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_h4(state):
    """Approve and send Horizon Media invoice INV-0056."""
    inv = find_invoice(state, "INV-0056")
    inv["status"] = "awaiting_payment"
    inv["sentAt"] = "2026-03-06T12:00:00Z"


def solve_task_h5(state):
    """Create monthly repeating invoice for Bright Spark Electrical."""
    contact = find_contact(state, "Bright Spark Electrical")
    rid = state["_nextRepeatId"]
    state["_nextRepeatId"] = rid + 1
    ri = {
        "id": f"rep_{rid:03d}",
        "contactId": contact["id"],
        "status": "draft",
        "frequency": "monthly",
        "startDate": "2026-04-01",
        "nextDate": "2026-04-01",
        "endDate": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "saveAs": "draft",
        "lineItems": [
            {
                "id": f"rli_{rid * 10}",
                "itemId": "item_004",
                "description": "Cloud Hosting - Monthly",
                "quantity": 1,
                "unitPrice": 299.00,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
            },
            {
                "id": f"rli_{rid * 10 + 1}",
                "itemId": "item_005",
                "description": "Technical Support - Monthly Plan",
                "quantity": 1,
                "unitPrice": 450.00,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
            },
        ],
        "dueDate": {"type": "daysAfterInvoice", "days": 30},
        "reference": "",
        "emailSubject": "",
        "emailBody": "",
    }
    state["repeatingInvoices"].append(ri)


def solve_task_h6(state):
    """Create invoice from accepted Alpha Logistics quote QU-0029."""
    quo = find_quote(state, "QU-0029")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    line_items = deepcopy(quo["lineItems"])
    for li in line_items:
        li["id"] = f"li_{lid}"
        lid += 1
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": quo["contactId"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": quo["reference"],
        "currency": quo["currency"],
        "brandingThemeId": quo["brandingThemeId"],
        "taxMode": quo["taxMode"],
        "lineItems": line_items,
        "subtotal": quo["subtotal"],
        "taxTotal": quo["taxTotal"],
        "total": quo["total"],
        "amountDue": quo["total"],
        "amountPaid": 0,
        "payments": [],
        "notes": [
            {"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-06T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_h7(state):
    """Record $5,000 partial payment on INV-0052 and set title."""
    inv = find_invoice(state, "INV-0052")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 5000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 5000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]
    inv["title"] = "March 2026 Development Sprint"


def solve_task_h8(state):
    """Create credit note for TechVault for 5 hours at $185, approve it."""
    contact = find_contact(state, "TechVault Solutions Pty Ltd")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 5 * 185.00
    tax = subtotal * 0.10
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_001",
            "description": "Software Development - Hourly Rate",
            "quantity": 5,
            "unitPrice": 185.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h9(state):
    """Fully pay INV-0048 ($4,180) and INV-0054 ($2,178)."""
    for inv_num, amount in [("INV-0048", 4180.00), ("INV-0054", 2178.00)]:
        inv = find_invoice(state, inv_num)
        pay_id = f"pay_{state['_nextPaymentId']}"
        state["_nextPaymentId"] += 1
        inv["payments"].append({
            "id": pay_id,
            "date": "2026-03-06",
            "amount": amount,
            "reference": "",
            "accountId": "acc_090",
        })
        inv["amountPaid"] += amount
        inv["amountDue"] = 0
        inv["status"] = "paid"


def solve_task_h10(state):
    """Create quote for NT Power Corp for security audit + 20 hours consulting, send it."""
    contact = find_contact(state, "Northern Territory Power Corp")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 5500.00 + 20 * 250.00
    tax = subtotal * 0.10
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "sent",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_009",
                "description": "Security Audit - Fixed Fee",
                "quantity": 1,
                "unitPrice": 5500.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_002",
                "description": "Consulting Services - Per Hour",
                "quantity": 20,
                "unitPrice": 250.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": "2026-03-06T12:00:00Z",
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h11(state):
    """Change invoice prefix to DEMO-, next number to 100, default due date to 14 days."""
    state["invoiceSettings"]["invoicePrefix"] = "DEMO-"
    state["invoiceSettings"]["invoiceNextNumber"] = 100
    state["invoiceSettings"]["defaultDueDate"] = {"type": "daysAfterInvoice", "days": 14}


def solve_task_h12(state):
    """Void all draft invoices."""
    for inv in state["invoices"]:
        if inv["status"] == "draft":
            inv["status"] = "voided"
            inv["amountDue"] = 0


def solve_task_h13(state):
    """Create quarterly repeating invoice for Southern Cross Veterinary."""
    contact = find_contact(state, "Southern Cross Veterinary")
    rid = state["_nextRepeatId"]
    state["_nextRepeatId"] = rid + 1
    ri = {
        "id": f"rep_{rid:03d}",
        "contactId": contact["id"],
        "status": "draft",
        "frequency": "quarterly",
        "startDate": "2026-04-01",
        "nextDate": "2026-04-01",
        "endDate": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "saveAs": "approved",
        "lineItems": [{
            "id": f"rli_{rid * 10}",
            "itemId": "item_005",
            "description": "Technical Support - Monthly Plan",
            "quantity": 1,
            "unitPrice": 450.00,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
        }],
        "dueDate": {"type": "daysAfterInvoice", "days": 30},
        "reference": "",
        "emailSubject": "",
        "emailBody": "",
    }
    state["repeatingInvoices"].append(ri)


def solve_task_h14(state):
    """Approve INV-0057, send it, record full payment."""
    inv = find_invoice(state, "INV-0057")
    inv["status"] = "paid"
    inv["sentAt"] = "2026-03-06T12:00:00Z"
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 6600.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] = 6600.00
    inv["amountDue"] = 0


def solve_task_h15(state):
    """Create invoice for Summit Health: annual license + 12 months support w/ 10% discount."""
    contact = find_contact(state, "Summit Health Group")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    license_subtotal = 1200.00
    support_subtotal = 12 * 450.00 * 0.90  # 10% discount
    subtotal = license_subtotal + support_subtotal
    tax = 0  # Summit Health uses GST Free
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_008",
                "description": "Software License - Annual",
                "quantity": 1,
                "unitPrice": 1200.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst_free",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_005",
                "description": "Technical Support - Monthly Plan",
                "quantity": 12,
                "unitPrice": 450.00,
                "discountPercent": 10,
                "accountId": "acc_200",
                "taxRateId": "tax_gst_free",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h16(state):
    """Delete all overdue reminders, keep only the before-due-date one."""
    state["invoiceReminders"] = [
        r for r in state["invoiceReminders"]
        if r["timing"] == "before"
    ]


def solve_task_h17(state):
    """Create 'Government' theme, disable payment advice, set as default."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Government",
        "isDefault": True,
        "logoUrl": "",
        "paymentTerms": "",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": False,
    }
    for t in state["brandingThemes"]:
        t["isDefault"] = False
    state["brandingThemes"].append(theme)


def solve_task_h18(state):
    """Copy INV-0047 to new draft, change contact to Cascade Software."""
    src = find_invoice(state, "INV-0047")
    cascade = find_contact(state, "Cascade Software Solutions")
    copy = deepcopy(src)
    num = state["_nextInvoiceNum"]
    copy["id"] = f"inv_{num:03d}"
    copy["number"] = state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}"
    state["_nextInvoiceNum"] = num + 1
    copy["status"] = "draft"
    copy["contactId"] = cascade["id"]
    copy["payments"] = []
    copy["amountPaid"] = 0
    copy["amountDue"] = copy["total"]
    copy["sentAt"] = None
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_h19(state):
    """Approve INV-0060, then record $1,000 partial payment."""
    inv = find_invoice(state, "INV-0060")
    inv["status"] = "awaiting_payment"
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 1000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 1000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]


def solve_task_h20(state):
    """Delete draft CN-0011, create new CN for Pacific Freight for $500."""
    cn_old = find_credit_note(state, "CN-0011")
    cn_old["status"] = "deleted"

    contact = find_contact(state, "Pacific Freight Lines")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 500.00
    tax = 50.00
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": None,
            "description": "Service credit",
            "quantity": 1,
            "unitPrice": 500.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h21(state):
    """Record full payment on CloudNine invoice with earliest due date (INV-0047)."""
    inv = find_invoice(state, "INV-0047")
    amount = inv["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": amount,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += amount
    inv["amountDue"] = 0
    inv["status"] = "paid"


def solve_task_h22(state):
    """Remove partial payment from INV-0045, then void it."""
    inv = find_invoice(state, "INV-0045")
    inv["payments"] = []
    inv["amountPaid"] = 0
    inv["amountDue"] = inv["total"]
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_h23(state):
    """Decline all sent quotes under $20,000."""
    for quo in state["quotes"]:
        if quo["status"] == "sent" and quo["total"] < 20000:
            quo["status"] = "declined"


def solve_task_h24(state):
    """Change all active repeating invoices to Professional Services theme."""
    for ri in state["repeatingInvoices"]:
        if ri["status"] == "active":
            ri["brandingThemeId"] = "theme_professional"


def solve_task_h25(state):
    """Create credit note for contact with largest outstanding balance for 5h consulting."""
    max_contact = max(state["contacts"], key=lambda c: c.get("outstandingBalance", 0))
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 5 * 250.00
    tax = subtotal * 0.10
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": max_contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_002",
            "description": "Consulting Services - Per Hour",
            "quantity": 5,
            "unitPrice": 250.00,
            "discountPercent": 0,
            "accountId": "acc_260",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h26(state):
    """Accept QU-0028 and create invoice from it."""
    quo = find_quote(state, "QU-0028")
    quo["status"] = "accepted"
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    line_items = deepcopy(quo["lineItems"])
    for li in line_items:
        li["id"] = f"li_{lid}"
        lid += 1
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": quo["contactId"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": quo["reference"],
        "currency": quo["currency"],
        "brandingThemeId": quo["brandingThemeId"],
        "taxMode": quo["taxMode"],
        "lineItems": line_items,
        "subtotal": quo["subtotal"],
        "taxTotal": quo["taxTotal"],
        "total": quo["total"],
        "amountDue": quo["total"],
        "amountPaid": 0,
        "payments": [],
        "notes": [
            {"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-06T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_h27(state):
    """Copy INV-0050 to new draft, update reference to ALI-2026-Q2."""
    src = find_invoice(state, "INV-0050")
    copy = deepcopy(src)
    num = state["_nextInvoiceNum"]
    copy["id"] = f"inv_{num:03d}"
    copy["number"] = state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}"
    state["_nextInvoiceNum"] = num + 1
    copy["status"] = "draft"
    copy["payments"] = []
    copy["amountPaid"] = 0
    copy["amountDue"] = copy["total"]
    copy["sentAt"] = None
    copy["reference"] = "ALI-2026-Q2"
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_h28(state):
    """Change quote prefix to EST- and create quote for Outback Adventures for 10 days PM."""
    state["invoiceSettings"]["quotePrefix"] = "EST-"
    contact = find_contact(state, "Outback Adventures Tourism")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 10 * 1400.00
    tax = subtotal * 0.10
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": "EST-" + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_003",
            "description": "Project Management - Day Rate",
            "quantity": 10,
            "unitPrice": 1400.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h29(state):
    """Change Vanguard Security repeating invoice to fortnightly, end date June 2026."""
    ri = find_repeating(state, "rep_004")
    ri["frequency"] = "fortnightly"
    ri["endDate"] = "2026-06-30"


def solve_task_h30(state):
    """Create 'Minimal' theme, disable tax number + payment advice, set as default."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Minimal",
        "isDefault": True,
        "logoUrl": "",
        "paymentTerms": "",
        "termsAndConditions": "",
        "showTaxNumber": False,
        "showPaymentAdvice": False,
    }
    for t in state["brandingThemes"]:
        t["isDefault"] = False
    state["brandingThemes"].append(theme)


def solve_task_h31(state):
    """Void TechVault invoice with security audit (INV-0055)."""
    inv = find_invoice(state, "INV-0055")
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_h32(state):
    """Create CN for Sapphire Bay $500, approve, allocate to INV-0054."""
    contact = find_contact(state, "Sapphire Bay Resort")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 500.00
    tax = 50.00
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": None,
            "description": "Service credit",
            "quantity": 1,
            "unitPrice": 500.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    inv = find_invoice(state, "INV-0054")
    alloc_amount = total
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": alloc_amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= alloc_amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += alloc_amount
    inv["amountDue"] -= alloc_amount
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h33(state):
    """Approve and send all invoices awaiting approval."""
    for inv in state["invoices"]:
        if inv["status"] == "awaiting_approval":
            inv["status"] = "awaiting_payment"
            inv["sentAt"] = "2026-03-06T12:00:00Z"


def solve_task_h34(state):
    """Set due date to 7 days after end of month, credit note prefix to CREDIT-."""
    state["invoiceSettings"]["defaultDueDate"] = {"type": "daysAfterEndOfMonth", "days": 7}
    state["invoiceSettings"]["creditNotePrefix"] = "CREDIT-"


def solve_task_h35(state):
    """Update QU-0024 title to 'Engineering Hub Platform v2'."""
    quo = find_quote(state, "QU-0024")
    quo["title"] = "Engineering Hub Platform v2"


def solve_task_h36(state):
    """Record $10,000 partial payment on INV-0055 and update summary."""
    inv = find_invoice(state, "INV-0055")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 10000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 10000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]
    inv["summary"] = "Partial payment received for Phase 2 development"


def solve_task_h37(state):
    """Fully pay INV-0061 (Greenfield Feb), void INV-0044 (Greenfield Jan)."""
    inv_061 = find_invoice(state, "INV-0061")
    amount = inv_061["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv_061["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": amount,
        "reference": "",
        "accountId": "acc_090",
    })
    inv_061["amountPaid"] += amount
    inv_061["amountDue"] = 0
    inv_061["status"] = "paid"
    inv_044 = find_invoice(state, "INV-0044")
    inv_044["status"] = "voided"
    inv_044["amountDue"] = 0


def solve_task_h38(state):
    """Fully pay INV-0050 (Alpha Logistics) and INV-0051 (Summit Health)."""
    for inv_num, amount in [("INV-0050", 13255.00), ("INV-0051", 6060.00)]:
        inv = find_invoice(state, inv_num)
        pay_id = f"pay_{state['_nextPaymentId']}"
        state["_nextPaymentId"] += 1
        inv["payments"].append({
            "id": pay_id,
            "date": "2026-03-06",
            "amount": amount,
            "reference": "",
            "accountId": "acc_090",
        })
        inv["amountPaid"] += amount
        inv["amountDue"] = 0
        inv["status"] = "paid"


def solve_task_h39(state):
    """Update reference on Greenfield e-commerce invoice (INV-0061) to GF-ECOM-2026."""
    inv = find_invoice(state, "INV-0061")
    inv["reference"] = "GF-ECOM-2026"


def solve_task_h40(state):
    """Create invoice for Outback Adventures: 5 days training (15% disc) + 40h dev, approve."""
    contact = find_contact(state, "Outback Adventures Tourism")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    training_subtotal = 5 * 2200.00 * 0.85
    dev_subtotal = 40 * 185.00
    subtotal = training_subtotal + dev_subtotal
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_006",
                "description": "On-site Training - Per Day",
                "quantity": 5,
                "unitPrice": 2200.00,
                "discountPercent": 15,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_001",
                "description": "Software Development - Hourly Rate",
                "quantity": 40,
                "unitPrice": 185.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h41(state):
    """Pay INV-0046, copy it, set reference BAX-Q2-2026 on copy."""
    inv = find_invoice(state, "INV-0046")
    remaining = inv["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": remaining,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += remaining
    inv["amountDue"] = 0
    inv["status"] = "paid"

    # Copy
    copy = deepcopy(inv)
    num = state["_nextInvoiceNum"]
    copy["id"] = f"inv_{num:03d}"
    copy["number"] = state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}"
    state["_nextInvoiceNum"] = num + 1
    copy["status"] = "draft"
    copy["payments"] = []
    copy["amountPaid"] = 0
    copy["amountDue"] = copy["total"]
    copy["sentAt"] = None
    copy["reference"] = "BAX-Q2-2026"
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {inv['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_h42(state):
    """Create invoice from most expensive uninvoiced accepted quote (QU-0022), approve+send."""
    quo = find_quote(state, "QU-0022")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    line_items = deepcopy(quo["lineItems"])
    for li in line_items:
        li["id"] = f"li_{lid}"
        lid += 1
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": quo["contactId"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": quo["reference"],
        "currency": quo["currency"],
        "brandingThemeId": quo["brandingThemeId"],
        "taxMode": quo["taxMode"],
        "lineItems": line_items,
        "subtotal": quo["subtotal"],
        "taxTotal": quo["taxTotal"],
        "total": quo["total"],
        "amountDue": quo["total"],
        "amountPaid": 0,
        "payments": [],
        "notes": [
            {"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-06T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": "2026-03-06T12:00:00Z",
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_h43(state):
    """Void INV-0049 (contains USB-C cables)."""
    inv = find_invoice(state, "INV-0049")
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_h44(state):
    """Allocate CN-0009 to INV-0049, then record $2,000 payment on INV-0049."""
    cn = find_credit_note(state, "CN-0009")
    inv = find_invoice(state, "INV-0049")
    amount = cn["remainingCredit"]
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += amount
    inv["amountDue"] -= amount

    # Record $2,000 payment
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 2000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 2000.00
    inv["amountDue"] -= 2000.00
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_h45(state):
    """Create invoice for Redback Mining (Perth, customer+supplier): 8h consulting + data migration, submit."""
    contact = find_contact(state, "Redback Mining Supplies")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 8 * 250.00 + 3800.00
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_approval",
        "date": "2026-03-06",
        "dueDate": "2026-04-20",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_002",
                "description": "Consulting Services - Per Hour",
                "quantity": 8,
                "unitPrice": 250.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_010",
                "description": "Data Migration Service",
                "quantity": 1,
                "unitPrice": 3800.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h46(state):
    """Send all draft quotes, approve all draft invoices."""
    for quo in state["quotes"]:
        if quo["status"] == "draft":
            quo["status"] = "sent"
            quo["sentAt"] = "2026-03-06T12:00:00Z"
    for inv in state["invoices"]:
        if inv["status"] == "draft":
            inv["status"] = "awaiting_payment"


def solve_task_h47(state):
    """Copy highest-value paid invoice (INV-0064, $23,100) to new draft, set reference REBILL-2026."""
    src = find_invoice(state, "INV-0064")
    copy = deepcopy(src)
    num = state["_nextInvoiceNum"]
    copy["id"] = f"inv_{num:03d}"
    copy["number"] = state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}"
    state["_nextInvoiceNum"] = num + 1
    copy["status"] = "draft"
    copy["payments"] = []
    copy["amountPaid"] = 0
    copy["amountDue"] = copy["total"]
    copy["sentAt"] = None
    copy["reference"] = "REBILL-2026"
    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_h48(state):
    """Approve CN-0011, allocate to INV-0048."""
    cn = find_credit_note(state, "CN-0011")
    cn["status"] = "awaiting_payment"
    inv = find_invoice(state, "INV-0048")
    amount = cn["total"]  # $968
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += amount
    inv["amountDue"] -= amount
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_h49(state):
    """Create quote for Bright Spark: 20h dev (5% disc) + 2 days training, send."""
    contact = find_contact(state, "Bright Spark Electrical")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    dev_subtotal = 20 * 185.00 * 0.95
    training_subtotal = 2 * 2200.00
    subtotal = dev_subtotal + training_subtotal
    tax = subtotal * 0.10
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "sent",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_001",
                "description": "Software Development - Hourly Rate",
                "quantity": 20,
                "unitPrice": 185.00,
                "discountPercent": 5,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_006",
                "description": "On-site Training - Per Day",
                "quantity": 2,
                "unitPrice": 2200.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": "2026-03-06T12:00:00Z",
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h50(state):
    """Update Cascade repeating invoice: fortnightly, end Sep 2026, saveAs draft."""
    ri = find_repeating(state, "rep_003")
    ri["frequency"] = "fortnightly"
    ri["endDate"] = "2026-09-30"
    ri["saveAs"] = "draft"


def solve_task_h51(state):
    """Enable tax number on all themes, disable payment advice on those that show it."""
    for t in state["brandingThemes"]:
        if t.get("showPaymentAdvice"):
            t["showPaymentAdvice"] = False
        t["showTaxNumber"] = True


def solve_task_h52(state):
    """Void paid TechVault invoice from before 2026 (INV-0043)."""
    inv = find_invoice(state, "INV-0043")
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_h53(state):
    """Delete Simple Clean + Retail themes, create 'Modern' with no payment advice."""
    state["brandingThemes"] = [
        t for t in state["brandingThemes"]
        if t["id"] not in ("theme_simple", "theme_retail")
    ]
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Modern",
        "isDefault": False,
        "logoUrl": "",
        "paymentTerms": "",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": False,
    }
    state["brandingThemes"].append(theme)


def solve_task_h54(state):
    """Record full payment on smallest outstanding invoice (INV-0053, $823.90)."""
    inv = find_invoice(state, "INV-0053")
    amount = inv["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": amount,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += amount
    inv["amountDue"] = 0
    inv["status"] = "paid"


def solve_task_h55(state):
    """Create 'NZ Export' theme, then invoice for Wellington in NZD using it."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "NZ Export",
        "isDefault": False,
        "logoUrl": "",
        "paymentTerms": "Net 60 days",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": True,
    }
    state["brandingThemes"].append(theme)

    contact = find_contact(state, "Wellington & Partners Accounting")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 8 * 250.00
    tax = 0  # Wellington is GST free
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "NZD",
        "brandingThemeId": f"theme_{tid}",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_002",
            "description": "Consulting Services - Per Hour",
            "quantity": 8,
            "unitPrice": 250.00,
            "discountPercent": 0,
            "accountId": "acc_260",
            "taxRateId": "tax_gst_free",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h56(state):
    """Record $15,000 payment on INV-0055 (Cloud Migration Phase 2)."""
    inv = find_invoice(state, "INV-0055")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 15000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 15000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]


def solve_task_h57(state):
    """Accept QU-0023, create invoice from it, record $5,000 payment."""
    quo = find_quote(state, "QU-0023")
    quo["status"] = "accepted"

    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    line_items = deepcopy(quo["lineItems"])
    for li in line_items:
        li["id"] = f"li_{lid}"
        lid += 1
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": quo["contactId"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-20",
        "reference": quo["reference"],
        "currency": quo["currency"],
        "brandingThemeId": quo["brandingThemeId"],
        "taxMode": quo["taxMode"],
        "lineItems": line_items,
        "subtotal": quo["subtotal"],
        "taxTotal": quo["taxTotal"],
        "total": quo["total"],
        "amountDue": quo["total"],
        "amountPaid": 0,
        "payments": [],
        "notes": [
            {"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-06T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True

    # Record $5,000 partial payment
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 5000.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 5000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]


def solve_task_h58(state):
    """Create 3-day before reminder, disable all after-due reminders."""
    rid = state["_nextReminderId"]
    state["_nextReminderId"] = rid + 1
    rem = {
        "id": f"rem_{rid:03d}",
        "enabled": True,
        "timing": "before",
        "days": 3,
        "subject": "Invoice due soon - {InvoiceNumber}",
        "body": "Dear {ContactName}, Invoice {InvoiceNumber} is due in 3 days.",
        "includeInvoicePdf": True,
        "includeSummary": True,
    }
    state["invoiceReminders"].append(rem)
    for r in state["invoiceReminders"]:
        if r["timing"] == "after":
            r["enabled"] = False


def solve_task_h59(state):
    """Change rep_002 (active, saves as draft) contact to Bright Spark Electrical."""
    ri = find_repeating(state, "rep_002")
    bright_spark = find_contact(state, "Bright Spark Electrical")
    ri["contactId"] = bright_spark["id"]


def solve_task_h60(state):
    """Create CN for Pinnacle (10h dev + 2d PM), approve, allocate to INV-0045."""
    contact = find_contact(state, "Pinnacle Construction Group")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    dev_subtotal = 10 * 185.00
    pm_subtotal = 2 * 1400.00
    subtotal = dev_subtotal + pm_subtotal
    tax = subtotal * 0.10
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_001",
                "description": "Software Development - Hourly Rate",
                "quantity": 10,
                "unitPrice": 185.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_003",
                "description": "Project Management - Day Rate",
                "quantity": 2,
                "unitPrice": 1400.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }

    # Allocate to INV-0045
    inv = find_invoice(state, "INV-0045")
    alloc_amount = total
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": alloc_amount,
        "date": "2026-03-06",
    })
    cn["remainingCredit"] -= alloc_amount
    if cn["remainingCredit"] <= 0.005:
        cn["status"] = "paid"
        cn["remainingCredit"] = 0
    inv["amountPaid"] += alloc_amount
    inv["amountDue"] -= alloc_amount
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0

    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h61(state):
    """Void all awaiting payment invoices overdue >2 weeks (due before 2026-02-20)."""
    from datetime import datetime, timedelta
    cutoff = datetime(2026, 2, 20)
    for inv in state["invoices"]:
        if inv["status"] != "awaiting_payment":
            continue
        due = datetime.strptime(inv["dueDate"], "%Y-%m-%d")
        if due < cutoff:
            inv["status"] = "voided"
            inv["amountDue"] = 0


def solve_task_h62(state):
    """Decline QU-0024 (most expensive sent) and create reduced-scope quote for Atlas Engineering."""
    quo = find_quote(state, "QU-0024")
    quo["status"] = "declined"

    contact = find_contact(state, "Atlas Engineering Consultants")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    dev_sub = 100 * 185.00
    pm_sub = 10 * 1400.00
    subtotal = dev_sub + pm_sub
    tax = subtotal * 0.10
    total = subtotal + tax
    new_quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_001",
                "description": "Software Development - Hourly Rate",
                "quantity": 100,
                "unitPrice": 185.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_003",
                "description": "Project Management - Day Rate",
                "quantity": 10,
                "unitPrice": 1400.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(new_quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h63(state):
    """Create credit note for Horizon Media (declined quote contact), 5h consulting, approve."""
    contact = find_contact(state, "Horizon Media & Advertising")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 5 * 250.00
    tax = subtotal * 0.10
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_002",
            "description": "Consulting Services - Per Hour",
            "quantity": 5,
            "unitPrice": 250.00,
            "discountPercent": 0,
            "accountId": "acc_260",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "remainingCredit": total,
        "allocations": [],
        "refunds": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h64(state):
    """Update rep_002 (saves as draft): frequency quarterly, reference QUARTERLY-REVIEW."""
    ri = find_repeating(state, "rep_002")
    ri["frequency"] = "quarterly"
    ri["reference"] = "QUARTERLY-REVIEW"


def solve_task_h65(state):
    """Decline QU-0028 (least expensive sent), accept QU-0024 (most expensive sent)."""
    quo_028 = find_quote(state, "QU-0028")
    quo_028["status"] = "declined"
    quo_024 = find_quote(state, "QU-0024")
    quo_024["status"] = "accepted"


def solve_task_h66(state):
    """Create monthly repeating invoice for Outback Adventures (Alice Springs) with hosting+support."""
    contact = find_contact(state, "Outback Adventures Tourism")
    rid = state["_nextRepeatId"]
    state["_nextRepeatId"] = rid + 1
    lid = state["_nextLineItemId"]
    rep = {
        "id": f"rep_{rid:03d}",
        "contactId": contact["id"],
        "status": "active",
        "frequency": "monthly",
        "startDate": "2026-03-06",
        "nextDate": "2026-04-06",
        "endDate": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "saveAs": "approved_for_sending",
        "lineItems": [
            {
                "id": f"rli_{lid}",
                "itemId": "item_004",
                "description": "Cloud Hosting - Monthly",
                "quantity": 1,
                "unitPrice": 299.00,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
            },
            {
                "id": f"rli_{lid + 1}",
                "itemId": "item_005",
                "description": "Technical Support - Monthly Plan",
                "quantity": 1,
                "unitPrice": 450.00,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
            },
        ],
        "dueDate": {"type": "daysAfterInvoice", "days": 30},
        "reference": "",
        "emailSubject": "",
        "emailBody": "",
    }
    state["repeatingInvoices"].append(rep)
    state["_nextLineItemId"] = lid + 2


def solve_task_h67(state):
    """Create invoice for Cascade Software (Canberra), 40h consulting + 3d PM, approve."""
    contact = find_contact(state, "Cascade Software Solutions")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    consult_sub = 40 * 250.00
    pm_sub = 3 * 1400.00
    subtotal = consult_sub + pm_sub
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-03-20",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_002",
                "description": "Consulting Services - Per Hour",
                "quantity": 40,
                "unitPrice": 250.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_003",
                "description": "Project Management - Day Rate",
                "quantity": 3,
                "unitPrice": 1400.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h68(state):
    """Record 25% payment on INV-0052 (Cascade dev sprint, $27,324)."""
    inv = find_invoice(state, "INV-0052")
    amount = 27324.00 / 4  # $6,831.00
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": amount,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += amount
    inv["amountDue"] -= amount


def solve_task_h69(state):
    """Record full payment on Perth-based awaiting_payment invoices (INV-0048, INV-0053)."""
    for num in ("INV-0048", "INV-0053"):
        inv = find_invoice(state, num)
        remaining = inv["amountDue"]
        pay_id = f"pay_{state['_nextPaymentId']}"
        state["_nextPaymentId"] += 1
        inv["payments"].append({
            "id": pay_id,
            "date": "2026-03-06",
            "amount": remaining,
            "reference": "",
            "accountId": "acc_090",
        })
        inv["amountPaid"] += remaining
        inv["amountDue"] = 0
        inv["status"] = "paid"


def solve_task_h70(state):
    """Change CN prefix to ADJ-, quote prefix to PROP-, create quote for Fresh Start Catering."""
    state["invoiceSettings"]["creditNotePrefix"] = "ADJ-"
    state["invoiceSettings"]["quotePrefix"] = "PROP-"

    contact = find_contact(state, "Fresh Start Catering Co")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 3 * 2200.00
    tax = subtotal * 0.10
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": "PROP-" + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_006",
            "description": "On-site Training - Per Day",
            "quantity": 3,
            "unitPrice": 2200.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h71(state):
    """Record $1,500 payment on INV-0048 (reference PF-WO-3301)."""
    inv = find_invoice(state, "INV-0048")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": 1500.00,
        "reference": "",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 1500.00
    inv["amountDue"] -= 1500.00


def solve_task_h72(state):
    """Create Healthcare theme with Net 60 days, update rep_005 to use it."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Healthcare",
        "isDefault": False,
        "logoUrl": "",
        "paymentTerms": "Net 60 days",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": True,
    }
    state["brandingThemes"].append(theme)

    ri = find_repeating(state, "rep_005")
    ri["brandingThemeId"] = f"theme_{tid}"


def solve_task_h73(state):
    """Add setup fee line item to INV-0058 and update title."""
    inv = find_invoice(state, "INV-0058")
    inv["title"] = "Website Redesign & Setup"

    lid = state["_nextLineItemId"]
    state["_nextLineItemId"] = lid + 1
    # INV-0058 is tax inclusive, so $500 inclusive = $454.55 + $45.45 GST
    inv["lineItems"].append({
        "id": f"li_{lid}",
        "itemId": "item_014",
        "description": "Initial Setup Fee",
        "quantity": 1,
        "unitPrice": 500.00,
        "discountPercent": 0,
        "accountId": "acc_200",
        "taxRateId": "tax_gst",
        "trackingRegion": "",
        "trackingDept": "",
    })
    inv["subtotal"] += 454.55
    inv["taxTotal"] += 45.45
    inv["total"] += 500.00
    inv["amountDue"] += 500.00


def solve_task_h74(state):
    """Create invoice for Southern Cross Vet: audit + 10h consulting, approve, send."""
    contact = find_contact(state, "Southern Cross Veterinary")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    audit_sub = 5500.00
    consult_sub = 10 * 250.00
    subtotal = audit_sub + consult_sub
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_009",
                "description": "Security Audit - Fixed Fee",
                "quantity": 1,
                "unitPrice": 5500.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_002",
                "description": "Consulting Services - Per Hour",
                "quantity": 10,
                "unitPrice": 250.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": "2026-03-06T12:00:00Z",
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h75(state):
    """Void CN-0009 (Coastal Living) and delete CN-0011 (Pacific Freight draft)."""
    cn_009 = find_credit_note(state, "CN-0009")
    cn_009["status"] = "voided"
    cn_009["remainingCredit"] = 0

    cn_011 = find_credit_note(state, "CN-0011")
    cn_011["status"] = "deleted"


def solve_task_h76(state):
    """Send QU-0025, copy to new draft, change copy's contact to Metro Fabrication."""
    src = find_quote(state, "QU-0025")
    src["status"] = "sent"
    src["sentAt"] = "2026-03-06T12:00:00Z"

    copy = deepcopy(src)
    num = state["_nextQuoteNum"]
    copy["id"] = f"quo_{num:03d}"
    copy["number"] = state["invoiceSettings"]["quotePrefix"] + f"{num:04d}"
    state["_nextQuoteNum"] = num + 1
    copy["status"] = "draft"
    copy["sentAt"] = None
    copy["isInvoiced"] = False

    metro = find_contact(state, "Metro Fabrication Works")
    copy["contactId"] = metro["id"]

    copy["notes"] = [{"date": "2026-03-06T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["quotes"].append(copy)


def solve_task_h77(state):
    """Create quote for NTP: audit + 30h dev (10% discount), Professional Services theme."""
    contact = find_contact(state, "Northern Territory Power Corp")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    audit_sub = 5500.00
    dev_gross = 30 * 185.00
    dev_net = dev_gross * 0.90
    net_subtotal = audit_sub + dev_net
    tax = net_subtotal * 0.10
    total = net_subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "expiryDate": "2026-04-05",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_professional",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_009",
                "description": "Security Audit - Fixed Fee",
                "quantity": 1,
                "unitPrice": 5500.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_001",
                "description": "Software Development - Hourly Rate",
                "quantity": 30,
                "unitPrice": 185.00,
                "discountPercent": 10,
                "accountId": "acc_200",
                "taxRateId": "tax_gst",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": net_subtotal,
        "taxTotal": tax,
        "total": total,
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h78(state):
    """Create NZD invoice for Wellington: data migration + 5h consulting, approve, send."""
    contact = find_contact(state, "Wellington & Partners Accounting")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    mig_sub = 3800.00
    consult_sub = 5 * 250.00
    subtotal = mig_sub + consult_sub
    tax = 0  # Wellington uses GST Free
    total = subtotal
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",
        "date": "2026-03-06",
        "dueDate": "2026-04-05",
        "reference": "",
        "currency": "NZD",
        "brandingThemeId": "theme_professional",
        "taxMode": "exclusive",
        "lineItems": [
            {
                "id": f"li_{lid}",
                "itemId": "item_010",
                "description": "Data Migration Service",
                "quantity": 1,
                "unitPrice": 3800.00,
                "discountPercent": 0,
                "accountId": "acc_200",
                "taxRateId": "tax_gst_free",
                "trackingRegion": "",
                "trackingDept": "",
            },
            {
                "id": f"li_{lid + 1}",
                "itemId": "item_002",
                "description": "Consulting Services - Per Hour",
                "quantity": 5,
                "unitPrice": 250.00,
                "discountPercent": 0,
                "accountId": "acc_260",
                "taxRateId": "tax_gst_free",
                "trackingRegion": "",
                "trackingDept": "",
            },
        ],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": "2026-03-06T12:00:00Z",
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 2


def solve_task_h79(state):
    """Change invoice prefix to AUS-, next number to 100, create invoice for CloudNine (8h design)."""
    state["invoiceSettings"]["invoicePrefix"] = "AUS-"
    state["invoiceSettings"]["invoiceNextNumber"] = 100

    contact = find_contact(state, "CloudNine Analytics")
    num = 100
    lid = state["_nextLineItemId"]
    subtotal = 8 * 165.00
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": f"AUS-{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-06",
        "dueDate": "2026-03-20",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_007",
            "description": "UI/UX Design - Hourly Rate",
            "quantity": 8,
            "unitPrice": 165.00,
            "discountPercent": 0,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
            "trackingRegion": "",
            "trackingDept": "",
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-06T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["invoiceSettings"]["invoiceNextNumber"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_h80(state):
    """Pay INV-0047 (earlier due), void INV-0062 (later due) — both CloudNine (Pitt Street)."""
    inv_0047 = find_invoice(state, "INV-0047")
    remaining = inv_0047["amountDue"]
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv_0047["payments"].append({
        "id": pay_id,
        "date": "2026-03-06",
        "amount": remaining,
        "reference": "",
        "accountId": "acc_090",
    })
    inv_0047["amountPaid"] += remaining
    inv_0047["amountDue"] = 0
    inv_0047["status"] = "paid"

    inv_0062 = find_invoice(state, "INV-0062")
    inv_0062["status"] = "voided"
    inv_0062["amountDue"] = 0


# ---------------------------------------------------------------------------
# Solver registry
# ---------------------------------------------------------------------------

SOLVERS = {}
for _prefix, _count in [("e", 20), ("m", 20), ("h", 80)]:
    for _i in range(1, _count + 1):
        _key = f"task_{_prefix}{_i}"
        _fn = globals().get(f"solve_{_key}")
        if _fn:
            SOLVERS[_key] = _fn

# ---------------------------------------------------------------------------
# Task loading and verification
# ---------------------------------------------------------------------------


def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    full_path = os.path.join(APP_DIR, verify_path)
    spec = importlib.util.spec_from_file_location("verifier", full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.verify


# ---------------------------------------------------------------------------
# Server management
# ---------------------------------------------------------------------------


def find_free_port(start=9500):
    port = start
    while port < start + 200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found starting from {start}")


def start_server(port, seed_state):
    proc = subprocess.Popen(
        [sys.executable, SERVER_PY, "--port", str(port)],
        cwd=APP_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    server_url = f"http://localhost:{port}"
    for _ in range(30):
        try:
            requests.post(f"{server_url}/api/reset", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    return proc


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# Task runner
# ---------------------------------------------------------------------------


def run_single_task(task, server_url):
    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver defined for {task_id}"

    try:
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"

        time.sleep(0.3)

        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()

        solver(state)

        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message

    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    proc = start_server(port, seed_state)
    server_url = f"http://localhost:{port}"
    results = []
    try:
        for task in tasks:
            tid, passed, msg = run_single_task(task, server_url)
            status = "\033[32m  PASS\033[0m" if passed else "\033[31m  FAIL\033[0m"
            print(f"{status}  {tid:12s} {msg}")
            results.append((tid, passed, msg))
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    results = []

    def worker_fn(task_batch, port):
        proc = start_server(port, seed_state)
        server_url = f"http://localhost:{port}"
        batch_results = []
        try:
            for task in task_batch:
                batch_results.append(run_single_task(task, server_url))
        finally:
            stop_server(proc)
        return batch_results

    batches = [[] for _ in range(workers)]
    for i, task in enumerate(tasks):
        batches[i % workers].append(task)

    ports = [find_free_port(base_port + i * 10) for i in range(workers)]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for i, batch in enumerate(batches):
            if batch:
                fut = executor.submit(worker_fn, batch, ports[i])
                futures[fut] = i

        for fut in as_completed(futures):
            try:
                batch_results = fut.result()
                for tid, passed, msg in batch_results:
                    status = "\033[32m  PASS\033[0m" if passed else "\033[31m  FAIL\033[0m"
                    print(f"{status}  {tid:12s} {msg}")
                    results.append((tid, passed, msg))
            except Exception as e:
                print(f"\033[31m  ERROR\033[0m Worker {futures[fut]}: {e}")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Xero Invoicing real-task sanity check")
    parser.add_argument("--task-id", type=str, help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--port", type=int, default=9500, help="Base port for servers")
    args = parser.parse_args()

    tasks = load_tasks()
    if args.task_id:
        tasks = [t for t in tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)

    print("Generating seed state from JS data...")
    seed_state = generate_seed_state()
    print(f"Running {len(tasks)} task(s)...\n")

    if args.workers <= 1:
        port = find_free_port(args.port)
        results = run_tasks_sequential(tasks, port, seed_state)
    else:
        results = run_tasks_parallel(tasks, args.workers, args.port, seed_state)

    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    failed = [tid for tid, p, _ in results if not p]

    print(f"\n{passed}/{total} passed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
