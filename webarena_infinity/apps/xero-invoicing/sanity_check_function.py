#!/usr/bin/env python3
"""
Sanity check for xero-invoicing function tasks.

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
TASKS_FILE = os.path.join(APP_DIR, "function-tasks.json")
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

def solve_task_1(state):
    """Approve draft invoice INV-0058."""
    inv = find_invoice(state, "INV-0058")
    inv["status"] = "awaiting_payment"


def solve_task_2(state):
    """Submit draft invoice INV-0060 for approval."""
    inv = find_invoice(state, "INV-0060")
    inv["status"] = "awaiting_approval"


def solve_task_3(state):
    """Approve awaiting_approval invoice INV-0056."""
    inv = find_invoice(state, "INV-0056")
    inv["status"] = "awaiting_payment"


def solve_task_4(state):
    """Void invoice INV-0054."""
    inv = find_invoice(state, "INV-0054")
    inv["status"] = "voided"
    inv["amountDue"] = 0


def solve_task_5(state):
    """Delete draft invoice INV-0059."""
    inv = find_invoice(state, "INV-0059")
    inv["status"] = "deleted"


def solve_task_6(state):
    """Copy invoice INV-0046 to new draft INV-0067."""
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
    copy["notes"] = [{"date": "2026-03-02T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["invoices"].append(copy)


def solve_task_7(state):
    """Record full payment of $823.90 on INV-0053."""
    inv = find_invoice(state, "INV-0053")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-02",
        "amount": 823.90,
        "reference": "EFT-VS-001",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 823.90
    inv["amountDue"] = inv["total"] - inv["amountPaid"]
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_8(state):
    """Record partial payment of $5,000 on INV-0052."""
    inv = find_invoice(state, "INV-0052")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-02",
        "amount": 5000.00,
        "reference": "PARTIAL-CSS",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 5000.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]


def solve_task_9(state):
    """Remove the $4,950 payment from INV-0045."""
    inv = find_invoice(state, "INV-0045")
    inv["payments"] = []
    inv["amountPaid"] = 0
    inv["amountDue"] = inv["total"]
    if inv["status"] == "paid":
        inv["status"] = "awaiting_payment"


def solve_task_10(state):
    """Create new invoice for TechVault with 10x DEV-HOUR."""
    contact = find_contact(state, "TechVault Solutions Pty Ltd")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 10 * 185.00
    tax = subtotal * 0.10
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-02",
        "dueDate": "2026-04-01",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
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
        }],
        "subtotal": subtotal,
        "taxTotal": tax,
        "total": total,
        "amountDue": total,
        "amountPaid": 0,
        "payments": [],
        "notes": [{"date": "2026-03-02T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_11(state):
    """Edit INV-0058 reference."""
    inv = find_invoice(state, "INV-0058")
    inv["reference"] = "MRW-WEB-MARCH"


def solve_task_12(state):
    """Mark INV-0057 as sent."""
    inv = find_invoice(state, "INV-0057")
    inv["status"] = "awaiting_payment"
    inv["sentAt"] = "2026-03-02T12:00:00Z"


def solve_task_13(state):
    """Create new invoice for Wellington & Partners in USD."""
    contact = find_contact(state, "Wellington & Partners Accounting")
    num = state["_nextInvoiceNum"]
    lid = state["_nextLineItemId"]
    subtotal = 12 * 250.00
    tax = 0  # GST Free
    total = subtotal + tax
    inv = {
        "id": f"inv_{num:03d}",
        "number": state["invoiceSettings"]["invoicePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-02",
        "dueDate": "2026-04-01",
        "reference": "",
        "currency": "USD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": "item_002",
            "description": "Consulting Services - Per Hour",
            "quantity": 12,
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
        "notes": [{"date": "2026-03-02T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "title": "",
        "summary": "",
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_14(state):
    """Record remaining $10,890 on INV-0045 to fully pay it."""
    inv = find_invoice(state, "INV-0045")
    pay_id = f"pay_{state['_nextPaymentId']}"
    state["_nextPaymentId"] += 1
    inv["payments"].append({
        "id": pay_id,
        "date": "2026-03-02",
        "amount": 10890.00,
        "reference": "EFT-FINAL",
        "accountId": "acc_090",
    })
    inv["amountPaid"] += 10890.00
    inv["amountDue"] = inv["total"] - inv["amountPaid"]
    if inv["amountDue"] <= 0.005:
        inv["status"] = "paid"
        inv["amountDue"] = 0


def solve_task_15(state):
    """Edit INV-0052 title."""
    inv = find_invoice(state, "INV-0052")
    inv["title"] = "March 2026 Development Sprint"


def solve_task_16(state):
    """Send draft quote QU-0025."""
    quo = find_quote(state, "QU-0025")
    quo["status"] = "sent"
    quo["sentAt"] = "2026-03-02T12:00:00Z"


def solve_task_17(state):
    """Accept quote QU-0023."""
    quo = find_quote(state, "QU-0023")
    quo["status"] = "accepted"


def solve_task_18(state):
    """Decline quote QU-0028."""
    quo = find_quote(state, "QU-0028")
    quo["status"] = "declined"


def solve_task_19(state):
    """Delete quote QU-0026."""
    quo = find_quote(state, "QU-0026")
    quo["status"] = "deleted"


def solve_task_20(state):
    """Copy quote QU-0024 to new draft QU-0030."""
    src = find_quote(state, "QU-0024")
    copy = deepcopy(src)
    num = state["_nextQuoteNum"]
    copy["id"] = f"quo_{num:03d}"
    copy["number"] = state["invoiceSettings"]["quotePrefix"] + f"{num:04d}"
    state["_nextQuoteNum"] = num + 1
    copy["status"] = "draft"
    copy["sentAt"] = None
    copy["isInvoiced"] = False
    copy["notes"] = [{"date": "2026-03-02T12:00:00Z", "text": f"Copied from {src['number']}", "user": "Sarah Mitchell"}]
    lid = state["_nextLineItemId"]
    for li in copy["lineItems"]:
        li["id"] = f"li_{lid}"
        lid += 1
    state["_nextLineItemId"] = lid
    state["quotes"].append(copy)


def solve_task_21(state):
    """Create invoice from accepted quote QU-0022."""
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
        "date": "2026-03-02",
        "dueDate": "2026-04-01",
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
            {"date": "2026-03-02T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-02T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_22(state):
    """Create new quote for Southern Cross Veterinary."""
    contact = find_contact(state, "Southern Cross Veterinary")
    num = state["_nextQuoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 8 * 250.00
    tax = 0  # GST Free
    total = subtotal + tax
    quo = {
        "id": f"quo_{num:03d}",
        "number": state["invoiceSettings"]["quotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-02",
        "expiryDate": "2026-04-01",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
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
        "title": "",
        "summary": "",
        "terms": "",
        "notes": [{"date": "2026-03-02T12:00:00Z", "text": "Quote created", "user": "Sarah Mitchell"}],
        "sentAt": None,
        "isInvoiced": False,
    }
    state["quotes"].append(quo)
    state["_nextQuoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_23(state):
    """Edit QU-0025 title."""
    quo = find_quote(state, "QU-0025")
    quo["title"] = "Online Catering Portal"


def solve_task_24(state):
    """Create invoice from accepted quote QU-0029."""
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
        "date": "2026-03-02",
        "dueDate": "2026-04-01",
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
            {"date": "2026-03-02T12:00:00Z", "text": "Invoice created", "user": "Sarah Mitchell"},
            {"date": "2026-03-02T12:00:01Z", "text": f"Created from quote {quo['number']}", "user": "Sarah Mitchell"},
        ],
        "sentAt": None,
        "title": quo["title"],
        "summary": quo["summary"],
    }
    state["invoices"].append(inv)
    state["_nextInvoiceNum"] = num + 1
    state["_nextLineItemId"] = lid
    quo["isInvoiced"] = True


def solve_task_25(state):
    """Approve draft credit note CN-0011."""
    cn = find_credit_note(state, "CN-0011")
    cn["status"] = "awaiting_payment"


def solve_task_26(state):
    """Allocate CN-0009 ($249.75) to INV-0049."""
    cn = find_credit_note(state, "CN-0009")
    inv = find_invoice(state, "INV-0049")
    amount = 249.75
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-02",
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


def solve_task_27(state):
    """Delete draft credit note CN-0011."""
    cn = find_credit_note(state, "CN-0011")
    cn["status"] = "deleted"


def solve_task_28(state):
    """Create new credit note for Greenfield Organics."""
    contact = find_contact(state, "Greenfield Organics")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 100.00
    tax = 10.00  # 10% GST
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "draft",
        "date": "2026-03-02",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": None,
            "description": "Hosting credit adjustment",
            "quantity": 1,
            "unitPrice": 100.00,
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
        "notes": [{"date": "2026-03-02T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_29(state):
    """Edit CN-0011 reference."""
    cn = find_credit_note(state, "CN-0011")
    cn["reference"] = "Feb-downtime-credit"


def solve_task_30(state):
    """Allocate CN-0012 ($2,035) to INV-0047."""
    cn = find_credit_note(state, "CN-0012")
    inv = find_invoice(state, "INV-0047")
    amount = 2035.00
    cn["allocations"].append({
        "invoiceId": inv["id"],
        "invoiceNumber": inv["number"],
        "amount": amount,
        "date": "2026-03-02",
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


def solve_task_31(state):
    """Create new credit note for TechVault and approve it."""
    contact = find_contact(state, "TechVault Solutions Pty Ltd")
    num = state["_nextCreditNoteNum"]
    lid = state["_nextLineItemId"]
    subtotal = 4 * 25.00
    tax = subtotal * 0.10
    total = subtotal + tax
    cn = {
        "id": f"cn_{num:03d}",
        "number": state["invoiceSettings"]["creditNotePrefix"] + f"{num:04d}",
        "contactId": contact["id"],
        "status": "awaiting_payment",  # approved directly
        "date": "2026-03-02",
        "reference": "",
        "currency": "AUD",
        "brandingThemeId": "theme_standard",
        "taxMode": "exclusive",
        "lineItems": [{
            "id": f"li_{lid}",
            "itemId": None,
            "description": "Rate adjustment",
            "quantity": 4,
            "unitPrice": 25.00,
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
        "notes": [{"date": "2026-03-02T12:00:00Z", "text": "Credit note created", "user": "Sarah Mitchell"}],
    }
    state["creditNotes"].append(cn)
    state["_nextCreditNoteNum"] = num + 1
    state["_nextLineItemId"] = lid + 1


def solve_task_32(state):
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
        "lineItems": [{
            "id": f"rli_{rid * 10}",
            "itemId": "item_004",
            "description": "Cloud Hosting - Monthly",
            "quantity": 1,
            "unitPrice": 299.00,
            "accountId": "acc_200",
            "taxRateId": "tax_gst",
        }],
        "dueDate": {"type": "daysAfterInvoice", "days": 30},
        "reference": "",
        "emailSubject": "",
        "emailBody": "",
    }
    state["repeatingInvoices"].append(ri)


def solve_task_33(state):
    """Edit rep_002 frequency to quarterly."""
    ri = find_repeating(state, "rep_002")
    ri["frequency"] = "quarterly"


def solve_task_34(state):
    """Delete repeating invoice rep_005."""
    state["repeatingInvoices"] = [r for r in state["repeatingInvoices"] if r["id"] != "rep_005"]


def solve_task_35(state):
    """Edit rep_001 end date."""
    ri = find_repeating(state, "rep_001")
    ri["endDate"] = "2027-06-30"


def solve_task_36(state):
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
            "taxRateId": "tax_gst_free",
        }],
        "dueDate": {"type": "daysAfterInvoice", "days": 30},
        "reference": "",
        "emailSubject": "",
        "emailBody": "",
    }
    state["repeatingInvoices"].append(ri)


def solve_task_37(state):
    """Edit rep_003 reference."""
    ri = find_repeating(state, "rep_003")
    ri["reference"] = "Cascade monthly license"


def solve_task_38(state):
    """Create branding theme 'Modern Minimalist'."""
    tid = state["_nextThemeId"]
    state["_nextThemeId"] = tid + 1
    theme = {
        "id": f"theme_{tid}",
        "name": "Modern Minimalist",
        "isDefault": False,
        "logoUrl": "",
        "paymentTerms": "Net 14 days",
        "termsAndConditions": "",
        "showTaxNumber": True,
        "showPaymentAdvice": True,
    }
    state["brandingThemes"].append(theme)


def solve_task_39(state):
    """Rename 'Retail' theme to 'Retail Premium'."""
    theme = find_theme(state, "theme_retail")
    theme["name"] = "Retail Premium"


def solve_task_40(state):
    """Set Professional Services as default theme."""
    for t in state["brandingThemes"]:
        t["isDefault"] = (t["id"] == "theme_professional")


def solve_task_41(state):
    """Delete Simple Clean theme."""
    state["brandingThemes"] = [t for t in state["brandingThemes"] if t["id"] != "theme_simple"]


def solve_task_42(state):
    """Disable showTaxNumber on Standard theme."""
    theme = find_theme(state, "theme_standard")
    theme["showTaxNumber"] = False


def solve_task_43(state):
    """Edit Professional Services terms and conditions."""
    theme = find_theme(state, "theme_professional")
    theme["termsAndConditions"] = "All work is subject to our Master Services Agreement. Payment terms are strictly net 30 days."


def solve_task_44(state):
    """Change invoice prefix to TAX-."""
    state["invoiceSettings"]["invoicePrefix"] = "TAX-"


def solve_task_45(state):
    """Change invoice next number to 100."""
    state["invoiceSettings"]["invoiceNextNumber"] = 100


def solve_task_46(state):
    """Change default due date to endOfFollowingMonth."""
    state["invoiceSettings"]["defaultDueDate"] = {"type": "endOfFollowingMonth", "days": 0}


def solve_task_47(state):
    """Change default tax mode to inclusive."""
    state["invoiceSettings"]["defaultTaxMode"] = "inclusive"


def solve_task_48(state):
    """Disable show tax column."""
    state["invoiceSettings"]["showTaxColumn"] = False


def solve_task_49(state):
    """Disable show discount column."""
    state["invoiceSettings"]["showDiscountColumn"] = False


def solve_task_50(state):
    """Disable show item code."""
    state["invoiceSettings"]["showItemCode"] = False


def solve_task_51(state):
    """Change credit note prefix to CR-."""
    state["invoiceSettings"]["creditNotePrefix"] = "CR-"


def solve_task_52(state):
    """Disable 7-day before reminder."""
    rem = find_reminder(state, "before", 7)
    rem["enabled"] = False


def solve_task_53(state):
    """Enable 30-day after reminder."""
    rem = find_reminder(state, "after", 30)
    rem["enabled"] = True


def solve_task_54(state):
    """Create new reminder for 21 days after."""
    rid = state["_nextReminderId"]
    state["_nextReminderId"] = rid + 1
    rem = {
        "id": f"rem_{rid:03d}",
        "enabled": True,
        "timing": "after",
        "days": 21,
        "subject": "Third reminder: Invoice overdue - {InvoiceNumber}",
        "body": "Dear {ContactName}, Invoice {InvoiceNumber} is now 21 days past due. Please arrange immediate payment.",
        "includeInvoicePdf": True,
        "includeSummary": True,
    }
    state["invoiceReminders"].append(rem)


def solve_task_55(state):
    """Delete 14-day after reminder."""
    state["invoiceReminders"] = [
        r for r in state["invoiceReminders"]
        if not (r["timing"] == "after" and r["days"] == 14)
    ]


def solve_task_56(state):
    """Edit 1-day after reminder subject."""
    rem = find_reminder(state, "after", 1)
    rem["subject"] = "Payment Required - {InvoiceNumber}"


def solve_task_57(state):
    """Edit QU-0025 expiry date."""
    quo = find_quote(state, "QU-0025")
    quo["expiryDate"] = "2026-04-30"


def solve_task_58(state):
    """Change quote prefix to QUOT-."""
    state["invoiceSettings"]["quotePrefix"] = "QUOT-"


# ---------------------------------------------------------------------------
# Solver registry
# ---------------------------------------------------------------------------

SOLVERS = {
    f"task_{i}": globals()[f"solve_task_{i}"]
    for i in range(1, 59)
}

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
    # Wait for server to accept connections
    server_url = f"http://localhost:{port}"
    for _ in range(30):
        try:
            requests.post(f"{server_url}/api/reset", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    # PUT seed state to establish _seed_state on the server
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
        # 1. Reset to seed state
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"

        time.sleep(0.3)

        # 2. Read seed state
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()

        # 3. Apply solve
        solver(state)

        # 4. Write solved state
        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        # 5. Run verifier
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

    # Partition tasks across workers
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
    parser = argparse.ArgumentParser(description="Xero Invoicing function-task sanity check")
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

    # Summary
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
