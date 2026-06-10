#!/usr/bin/env python3
"""
Sanity check for paypal-my-wallet function tasks.

For each task: reset -> apply solve (state mutation) -> verify -> assert pass.
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
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    cards: JSON.parse(JSON.stringify(CARDS)),
    bankAccounts: JSON.parse(JSON.stringify(BANK_ACCOUNTS)),
    balances: JSON.parse(JSON.stringify(BALANCES)),
    cryptoHoldings: JSON.parse(JSON.stringify(CRYPTO_HOLDINGS)),
    paypalDebitCard: JSON.parse(JSON.stringify(PAYPAL_DEBIT_CARD)),
    savingsAccount: JSON.parse(JSON.stringify(SAVINGS_ACCOUNT)),
    payLaterPlans: JSON.parse(JSON.stringify(PAY_LATER_PLANS)),
    rewards: JSON.parse(JSON.stringify(REWARDS)),
    offers: JSON.parse(JSON.stringify(OFFERS)),
    giftCards: JSON.parse(JSON.stringify(GIFT_CARDS)),
    transactions: JSON.parse(JSON.stringify(TRANSACTIONS)),
    paypalCredit: JSON.parse(JSON.stringify(PAYPAL_CREDIT)),
    walletPreferences: JSON.parse(JSON.stringify(WALLET_PREFERENCES)),
    giftCardMerchants: JSON.parse(JSON.stringify(GIFT_CARD_MERCHANTS)),
    _nextCardId: 100,
    _nextBankId: 100,
    _nextTransactionId: 200,
    _nextGiftCardId: 100,
    _nextOfferId: 100,
    _nextRewardId: 100,
    _nextCryptoTxId: 200,
    _nextSavingsTxId: 100,
    _nextPlanId: 100,
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


def find_card(state, lastFour):
    return find_entity(state["cards"], lastFour=lastFour)


def find_bank(state, lastFour):
    return find_entity(state["bankAccounts"], lastFour=lastFour)


def find_balance(state, currency):
    return find_entity(state["balances"], currency=currency)


def find_crypto(state, symbol):
    return find_entity(state["cryptoHoldings"], symbol=symbol)


def find_offer(state, merchantName):
    return find_entity(state["offers"], merchantName=merchantName)


def now_iso():
    return "2026-03-07T12:00:00Z"


# ---------------------------------------------------------------------------
# Crypto fee calculation (mirrors state.js logic)
# ---------------------------------------------------------------------------

CRYPTO_FEE_SCHEDULE = [
    {"minAmount": 1, "maxAmount": 4.99, "fee": 0.49},
    {"minAmount": 5, "maxAmount": 24.99, "fee": 0.99},
    {"minAmount": 25, "maxAmount": 74.99, "fee": 1.99},
    {"minAmount": 75, "maxAmount": 200, "fee": 2.49},
    {"minAmount": 200.01, "maxAmount": None, "feePercent": 1.50},
]


def calculate_crypto_fee(amount):
    for tier in CRYPTO_FEE_SCHEDULE:
        if amount >= tier["minAmount"] and (tier["maxAmount"] is None or amount <= tier["maxAmount"]):
            if "feePercent" in tier:
                return round(amount * tier["feePercent"]) / 100
            return tier["fee"]
    return 0


# ---------------------------------------------------------------------------
# Solve functions — one per task, derived from verifiers
# ---------------------------------------------------------------------------

def solve_task_1(state):
    """Set Mastercard ****7156 as preferred card."""
    for c in state["cards"]:
        c["isPreferred"] = False
    card = find_card(state, "7156")
    card["isPreferred"] = True
    state["walletPreferences"]["preferredPaymentMethod"] = card["id"]
    state["currentUser"]["preferredPaymentMethodId"] = card["id"]


def solve_task_2(state):
    """Set Amex ****3001 as backup card."""
    for c in state["cards"]:
        c["isBackup"] = False
    card = find_card(state, "3001")
    card["isBackup"] = True
    state["walletPreferences"]["backupPaymentMethod"] = card["id"]
    state["currentUser"]["backupPaymentMethodId"] = card["id"]


def solve_task_3(state):
    """Remove expired Discover ****6221."""
    state["cards"] = [c for c in state["cards"] if c["lastFour"] != "6221"]


def solve_task_4(state):
    """Confirm pending Visa ****8834."""
    card = find_card(state, "8834")
    card["status"] = "confirmed"
    card["confirmedAt"] = now_iso()


def solve_task_5(state):
    """Add new Visa credit card ****9999."""
    card_id = f"card_{state['_nextCardId']:03d}"
    state["_nextCardId"] += 1
    state["cards"].append({
        "id": card_id,
        "type": "credit",
        "brand": "Visa",
        "lastFour": "9999",
        "cardholderName": "Jordan Mitchell",
        "expirationMonth": 12,
        "expirationYear": 2030,
        "billingAddress": {
            "street": "500 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94108",
            "country": "US"
        },
        "status": "pending_confirmation",
        "isPreferred": False,
        "isExpired": False,
        "addedAt": now_iso(),
        "confirmedAt": None,
        "lastUsed": None,
        "isBackup": False,
        "confirmationCode": None
    })


def solve_task_6(state):
    """Update Amex ****3001 billing address."""
    card = find_card(state, "3001")
    card["billingAddress"] = {
        "street": "100 Market St",
        "city": "San Jose",
        "state": "CA",
        "zip": "95110",
        "country": "US"
    }


def solve_task_7(state):
    """Remove preferred Visa ****4829 (side effect: clears preferred)."""
    state["cards"] = [c for c in state["cards"] if c["lastFour"] != "4829"]
    state["walletPreferences"]["preferredPaymentMethod"] = None


def solve_task_8(state):
    """Confirm pending Wells Fargo ****5518."""
    bank = find_bank(state, "5518")
    bank["status"] = "confirmed"
    bank["confirmedAt"] = now_iso()
    bank["confirmationDeposit1"] = 0.12
    bank["confirmationDeposit2"] = 0.34


def solve_task_9(state):
    """Remove Citibank ****1104."""
    state["bankAccounts"] = [b for b in state["bankAccounts"] if b["lastFour"] != "1104"]


def solve_task_10(state):
    """Remove Chase ****6742 (side effect: clears backup)."""
    state["bankAccounts"] = [b for b in state["bankAccounts"] if b["lastFour"] != "6742"]
    state["walletPreferences"]["backupPaymentMethod"] = None


def solve_task_11(state):
    """Add TD Bank checking ****4455."""
    bank_id = f"bank_{state['_nextBankId']:03d}"
    state["_nextBankId"] += 1
    state["bankAccounts"].append({
        "id": bank_id,
        "bankName": "TD Bank",
        "accountType": "checking",
        "lastFour": "4455",
        "routingNumber": "031201360",
        "status": "pending_confirmation",
        "isPreferred": False,
        "addedAt": now_iso(),
        "confirmedAt": None,
        "lastUsed": None,
        "confirmationDeposit1": None,
        "confirmationDeposit2": None,
        "instantTransferEligible": False
    })


def solve_task_12(state):
    """Add $500 from Chase to balance."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] + 500) * 100) / 100
    bank = find_bank(state, "6742")
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "transfer_in",
        "description": f"From {bank['bankName']} ***{bank['lastFour']}",
        "amount": 500,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": bank["id"],
        "category": "Transfer"
    })


def solve_task_13(state):
    """Withdraw $200 to Bank of America."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] - 200) * 100) / 100
    bank = find_bank(state, "3891")
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "transfer_out",
        "description": f"To {bank['bankName']} ***{bank['lastFour']}",
        "amount": -200,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": bank["id"],
        "category": "Transfer"
    })


def solve_task_14(state):
    """Convert $100 USD to EUR."""
    usd = find_balance(state, "USD")
    eur = find_balance(state, "EUR")
    amount = 100
    from_rate = 1.0  # USD
    to_rate = 0.92   # EUR
    usd_amount = amount / from_rate
    converted = usd_amount * to_rate
    fee = usd_amount * 0.03
    usd["amount"] = round((usd["amount"] - amount) * 100) / 100
    eur["amount"] = round((eur["amount"] + converted - (fee * to_rate)) * 100) / 100
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "currency_convert",
        "description": "Converted USD to EUR",
        "amount": -amount,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Currency"
    })


def solve_task_15(state):
    """Add CHF currency."""
    state["balances"].append({
        "currency": "CHF",
        "amount": 0,
        "isPrimary": False
    })


def solve_task_16(state):
    """Remove CAD currency (zero balance)."""
    state["balances"] = [b for b in state["balances"] if b["currency"] != "CAD"]


def solve_task_17(state):
    """Set EUR as primary currency."""
    for b in state["balances"]:
        b["isPrimary"] = False
    eur = find_balance(state, "EUR")
    eur["isPrimary"] = True
    state["currentUser"]["primaryCurrency"] = "EUR"


def solve_task_18(state):
    """Buy $100 of BTC."""
    usd = find_balance(state, "USD")
    btc = find_crypto(state, "BTC")
    usd_amount = 100
    fee = calculate_crypto_fee(usd_amount)
    net_amount = usd_amount - fee
    quantity = net_amount / btc["currentPrice"]
    usd["amount"] = round((usd["amount"] - usd_amount) * 100) / 100
    btc["quantity"] = round((btc["quantity"] + quantity) * 100000) / 100000
    btc["totalCost"] = round((btc["totalCost"] + net_amount) * 100) / 100
    btc["currentValue"] = round(btc["quantity"] * btc["currentPrice"] * 100) / 100
    btc["totalReturn"] = round((btc["currentValue"] - btc["totalCost"]) * 100) / 100
    btc["totalReturnPercent"] = round((btc["totalReturn"] / btc["totalCost"]) * 10000) / 100 if btc["totalCost"] > 0 else 0
    btc["averagePurchasePrice"] = round((btc["totalCost"] / btc["quantity"]) * 100) / 100 if btc["quantity"] > 0 else 0
    ctx_id = f"ctx_{state['_nextCryptoTxId']:03d}"
    state["_nextCryptoTxId"] += 1
    btc["transactions"].append({
        "id": ctx_id,
        "type": "buy",
        "quantity": quantity,
        "pricePerUnit": btc["currentPrice"],
        "total": net_amount,
        "fee": fee,
        "date": now_iso()
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "crypto_buy",
        "description": f"Bought {btc['name']}",
        "amount": -usd_amount,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Crypto"
    })


def solve_task_19(state):
    """Sell $50 of ETH."""
    usd = find_balance(state, "USD")
    eth = find_crypto(state, "ETH")
    usd_amount = 50
    quantity = usd_amount / eth["currentPrice"]
    fee = calculate_crypto_fee(usd_amount)
    net_proceeds = usd_amount - fee
    cost_basis = quantity * eth["averagePurchasePrice"]
    eth["quantity"] = round((eth["quantity"] - quantity) * 100000) / 100000
    eth["totalCost"] = max(0, round((eth["totalCost"] - cost_basis) * 100) / 100)
    eth["currentValue"] = round(eth["quantity"] * eth["currentPrice"] * 100) / 100
    eth["totalReturn"] = round((eth["currentValue"] - eth["totalCost"]) * 100) / 100
    eth["totalReturnPercent"] = round((eth["totalReturn"] / eth["totalCost"]) * 10000) / 100 if eth["totalCost"] > 0 else 0
    usd["amount"] = round((usd["amount"] + net_proceeds) * 100) / 100
    ctx_id = f"ctx_{state['_nextCryptoTxId']:03d}"
    state["_nextCryptoTxId"] += 1
    eth["transactions"].append({
        "id": ctx_id,
        "type": "sell",
        "quantity": quantity,
        "pricePerUnit": eth["currentPrice"],
        "total": net_proceeds,
        "fee": fee,
        "date": now_iso()
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "crypto_sell",
        "description": f"Sold {eth['name']}",
        "amount": net_proceeds,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Crypto"
    })


def solve_task_20(state):
    """Buy $25 of SOL."""
    usd = find_balance(state, "USD")
    sol = find_crypto(state, "SOL")
    usd_amount = 25
    fee = calculate_crypto_fee(usd_amount)
    net_amount = usd_amount - fee
    quantity = net_amount / sol["currentPrice"]
    usd["amount"] = round((usd["amount"] - usd_amount) * 100) / 100
    sol["quantity"] = round((sol["quantity"] + quantity) * 100000) / 100000
    sol["totalCost"] = round((sol["totalCost"] + net_amount) * 100) / 100
    sol["currentValue"] = round(sol["quantity"] * sol["currentPrice"] * 100) / 100
    sol["totalReturn"] = round((sol["currentValue"] - sol["totalCost"]) * 100) / 100
    sol["totalReturnPercent"] = round((sol["totalReturn"] / sol["totalCost"]) * 10000) / 100 if sol["totalCost"] > 0 else 0
    sol["averagePurchasePrice"] = round((sol["totalCost"] / sol["quantity"]) * 100) / 100 if sol["quantity"] > 0 else 0
    ctx_id = f"ctx_{state['_nextCryptoTxId']:03d}"
    state["_nextCryptoTxId"] += 1
    sol["transactions"].append({
        "id": ctx_id,
        "type": "buy",
        "quantity": quantity,
        "pricePerUnit": sol["currentPrice"],
        "total": net_amount,
        "fee": fee,
        "date": now_iso()
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "crypto_buy",
        "description": f"Bought {sol['name']}",
        "amount": -usd_amount,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Crypto"
    })


def solve_task_21(state):
    """Sell $100 of LTC."""
    usd = find_balance(state, "USD")
    ltc = find_crypto(state, "LTC")
    usd_amount = 100
    quantity = usd_amount / ltc["currentPrice"]
    fee = calculate_crypto_fee(usd_amount)
    net_proceeds = usd_amount - fee
    cost_basis = quantity * ltc["averagePurchasePrice"]
    ltc["quantity"] = round((ltc["quantity"] - quantity) * 100000) / 100000
    ltc["totalCost"] = max(0, round((ltc["totalCost"] - cost_basis) * 100) / 100)
    ltc["currentValue"] = round(ltc["quantity"] * ltc["currentPrice"] * 100) / 100
    ltc["totalReturn"] = round((ltc["currentValue"] - ltc["totalCost"]) * 100) / 100
    ltc["totalReturnPercent"] = round((ltc["totalReturn"] / ltc["totalCost"]) * 10000) / 100 if ltc["totalCost"] > 0 else 0
    usd["amount"] = round((usd["amount"] + net_proceeds) * 100) / 100
    ctx_id = f"ctx_{state['_nextCryptoTxId']:03d}"
    state["_nextCryptoTxId"] += 1
    ltc["transactions"].append({
        "id": ctx_id,
        "type": "sell",
        "quantity": quantity,
        "pricePerUnit": ltc["currentPrice"],
        "total": net_proceeds,
        "fee": fee,
        "date": now_iso()
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "crypto_sell",
        "description": f"Sold {ltc['name']}",
        "amount": net_proceeds,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Crypto"
    })


def solve_task_22(state):
    """Deposit $500 to savings."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] - 500) * 100) / 100
    state["savingsAccount"]["balance"] = round((state["savingsAccount"]["balance"] + 500) * 100) / 100
    stx_id = f"stx_{state['_nextSavingsTxId']:03d}"
    state["_nextSavingsTxId"] += 1
    state["savingsAccount"]["transferHistory"].append({
        "id": stx_id,
        "type": "deposit",
        "amount": 500,
        "date": now_iso(),
        "from": "PayPal Balance"
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "savings_deposit",
        "description": "Transfer to Savings",
        "amount": -500,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Savings"
    })


def solve_task_23(state):
    """Withdraw $1000 from savings."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] + 1000) * 100) / 100
    state["savingsAccount"]["balance"] = round((state["savingsAccount"]["balance"] - 1000) * 100) / 100
    stx_id = f"stx_{state['_nextSavingsTxId']:03d}"
    state["_nextSavingsTxId"] += 1
    state["savingsAccount"]["transferHistory"].append({
        "id": stx_id,
        "type": "withdrawal",
        "amount": 1000,
        "date": now_iso(),
        "to": "PayPal Balance"
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "savings_withdrawal",
        "description": "Transfer from Savings",
        "amount": 1000,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Savings"
    })


def solve_task_24(state):
    """Set daily spending limit to $5000."""
    state["paypalDebitCard"]["dailySpendingLimit"] = 5000


def solve_task_25(state):
    """Set daily ATM limit to $300."""
    state["paypalDebitCard"]["dailyATMLimit"] = 300


def solve_task_26(state):
    """Disable cash back."""
    state["paypalDebitCard"]["cashBackEnabled"] = False


def solve_task_27(state):
    """Change employer to Acme Corp."""
    state["paypalDebitCard"]["directDeposit"]["employer"] = "Acme Corp"


def solve_task_28(state):
    """Disable direct deposit."""
    state["paypalDebitCard"]["directDeposit"]["enabled"] = False


def solve_task_29(state):
    """Change cash back category to Groceries."""
    state["paypalDebitCard"]["cashBackCategory"] = "Groceries"


def solve_task_30(state):
    """Make $100 PayPal Credit payment."""
    usd = find_balance(state, "USD")
    pc = state["paypalCredit"]
    usd["amount"] = round((usd["amount"] - 100) * 100) / 100
    pc["currentBalance"] = max(0, round((pc["currentBalance"] - 100) * 100) / 100)
    pc["availableCredit"] = round((pc["creditLimit"] - pc["currentBalance"]) * 100) / 100
    pc["lastPaymentAmount"] = 100
    pc["lastPaymentDate"] = now_iso()


def solve_task_31(state):
    """Disable autopay."""
    state["paypalCredit"]["autopayEnabled"] = False


def solve_task_32(state):
    """Set autopay amount to full."""
    state["paypalCredit"]["autopayAmount"] = "full"


def solve_task_33(state):
    """Make minimum payment of $35."""
    usd = find_balance(state, "USD")
    pc = state["paypalCredit"]
    usd["amount"] = round((usd["amount"] - 35) * 100) / 100
    pc["currentBalance"] = max(0, round((pc["currentBalance"] - 35) * 100) / 100)
    pc["availableCredit"] = round((pc["creditLimit"] - pc["currentBalance"]) * 100) / 100
    pc["lastPaymentAmount"] = 35
    pc["lastPaymentDate"] = now_iso()


def solve_task_34(state):
    """Save DoorDash offer."""
    offer = find_offer(state, "DoorDash")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_35(state):
    """Unsave Starbucks offer."""
    offer = find_offer(state, "Starbucks")
    offer["status"] = "available"
    offer["savedAt"] = None


def solve_task_36(state):
    """Save Nike offer."""
    offer = find_offer(state, "Nike")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_37(state):
    """Save Target offer."""
    offer = find_offer(state, "Target")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_38(state):
    """Unsave Uber offer."""
    offer = find_offer(state, "Uber")
    offer["status"] = "available"
    offer["savedAt"] = None


def solve_task_39(state):
    """Save Amazon offer."""
    offer = find_offer(state, "Amazon")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_40(state):
    """Redeem 500 pts for PayPal balance."""
    rewards = state["rewards"]
    rewards["totalPoints"] -= 500
    rewards["pointsValue"] = round(rewards["totalPoints"]) / 100
    rwd_id = f"rwd_{state['_nextRewardId']:03d}"
    state["_nextRewardId"] += 1
    rewards["history"].insert(0, {
        "id": rwd_id,
        "description": "Redeemed for PayPal Balance",
        "points": -500,
        "date": now_iso(),
        "type": "redeemed",
        "redemptionValue": 5.00
    })
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] + 5.00) * 100) / 100


def solve_task_41(state):
    """Redeem 1000 pts for gift card."""
    rewards = state["rewards"]
    rewards["totalPoints"] -= 1000
    rewards["pointsValue"] = round(rewards["totalPoints"]) / 100
    rwd_id = f"rwd_{state['_nextRewardId']:03d}"
    state["_nextRewardId"] += 1
    rewards["history"].insert(0, {
        "id": rwd_id,
        "description": "Redeemed for Gift Card",
        "points": -1000,
        "date": now_iso(),
        "type": "redeemed",
        "redemptionValue": 10.00
    })


def solve_task_42(state):
    """Purchase $50 Amazon gift card for alex.johnson@email.com."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] - 50) * 100) / 100
    gc_id = f"gc_{state['_nextGiftCardId']:03d}"
    state["_nextGiftCardId"] += 1
    state["giftCards"].insert(0, {
        "id": gc_id,
        "merchantName": "Amazon",
        "amount": 50,
        "remainingBalance": 50,
        "status": "active",
        "purchasedAt": now_iso(),
        "recipientEmail": "alex.johnson@email.com",
        "recipientName": "Alex Johnson",
        "senderName": "Jordan Mitchell",
        "message": "Happy Birthday!",
        "redemptionCode": "AMZ-TEST-TEST-TEST",
        "redeemed": False
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "gift_card",
        "description": "Gift Card - Amazon",
        "amount": -50,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Gift Cards"
    })


def solve_task_43(state):
    """Purchase $25 Starbucks gift card for self."""
    usd = find_balance(state, "USD")
    usd["amount"] = round((usd["amount"] - 25) * 100) / 100
    gc_id = f"gc_{state['_nextGiftCardId']:03d}"
    state["_nextGiftCardId"] += 1
    state["giftCards"].insert(0, {
        "id": gc_id,
        "merchantName": "Starbucks",
        "amount": 25,
        "remainingBalance": 25,
        "status": "active",
        "purchasedAt": now_iso(),
        "recipientEmail": "jordan.mitchell@outlook.com",
        "recipientName": "Jordan Mitchell",
        "senderName": "Jordan Mitchell",
        "message": "",
        "redemptionCode": "SBX-TEST-TEST-TEST",
        "redeemed": False
    })
    txn_id = f"txn_{state['_nextTransactionId']:03d}"
    state["_nextTransactionId"] += 1
    state["transactions"].insert(0, {
        "id": txn_id,
        "type": "gift_card",
        "description": "Gift Card - Starbucks",
        "amount": -25,
        "currency": "USD",
        "date": now_iso(),
        "status": "completed",
        "paymentMethod": "balance",
        "category": "Gift Cards"
    })


def solve_task_44(state):
    """Set preferred payment to Amex ****3001 via preferences."""
    for c in state["cards"]:
        c["isPreferred"] = False
    card = find_card(state, "3001")
    card["isPreferred"] = True
    state["walletPreferences"]["preferredPaymentMethod"] = card["id"]
    state["currentUser"]["preferredPaymentMethodId"] = card["id"]


def solve_task_45(state):
    """Set backup payment to Chase ****6742 via preferences."""
    # bank_001 is already the backup, but we confirm it's set correctly
    for c in state["cards"]:
        c["isBackup"] = False
    bank = find_bank(state, "6742")
    state["walletPreferences"]["backupPaymentMethod"] = bank["id"]
    state["currentUser"]["backupPaymentMethodId"] = bank["id"]


def solve_task_46(state):
    """Disable auto-accept payments."""
    state["walletPreferences"]["autoAcceptPayments"] = False


def solve_task_47(state):
    """Disable instant transfer preference."""
    state["walletPreferences"]["instantTransferPreference"] = False


def solve_task_48(state):
    """Set currency conversion to card_issuer."""
    state["walletPreferences"]["currencyConversionOption"] = "card_issuer"


def solve_task_49(state):
    """Disable payment email notifications."""
    state["walletPreferences"]["emailNotifications"]["payments"] = False


def solve_task_50(state):
    """Enable promotions email notifications."""
    state["walletPreferences"]["emailNotifications"]["promotions"] = True


def solve_task_51(state):
    """Disable weekly digest."""
    state["walletPreferences"]["emailNotifications"]["weeklyDigest"] = False


def solve_task_52(state):
    """Disable crypto alerts."""
    state["walletPreferences"]["emailNotifications"]["cryptoAlerts"] = False


def solve_task_53(state):
    """Disable rewards updates."""
    state["walletPreferences"]["emailNotifications"]["rewardsUpdates"] = False


def solve_task_54(state):
    """Save Chipotle offer."""
    offer = find_offer(state, "Chipotle")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_55(state):
    """Save Walmart offer."""
    offer = find_offer(state, "Walmart")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


def solve_task_56(state):
    """Save Lyft offer."""
    offer = find_offer(state, "Lyft")
    offer["status"] = "saved"
    offer["savedAt"] = now_iso()


# ---------------------------------------------------------------------------
# Solver registry
# ---------------------------------------------------------------------------

SOLVERS = {
    f"task_{i}": globals()[f"solve_task_{i}"]
    for i in range(1, 57)
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
    parser = argparse.ArgumentParser(description="PayPal My Wallet function-task sanity check")
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
