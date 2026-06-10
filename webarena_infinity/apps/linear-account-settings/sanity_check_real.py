#!/usr/bin/env python3
"""
Sanity check for Linear Account Settings real-task verifiers.

For each task, directly constructs the expected end-state (bypassing the agent),
then runs the verifier and asserts it returns True.

Usage:
    python3 sanity_check_real.py                      # All tasks, sequential
    python3 sanity_check_real.py --workers N           # N parallel environments
    python3 sanity_check_real.py --task-id <id>        # Single task (for debugging)
    python3 sanity_check_real.py --port <base>         # Custom base port
"""
import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "real-tasks.json"

# JS snippet to evaluate data.js and emit the seed state as JSON
_SEED_STATE_JS = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

const state = {
    _seedVersion: SEED_DATA_VERSION,
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    workspaces: JSON.parse(JSON.stringify(WORKSPACES)),
    connectedAccounts: JSON.parse(JSON.stringify(CONNECTED_ACCOUNTS)),
    preferences: JSON.parse(JSON.stringify(PREFERENCES)),
    notificationSettings: JSON.parse(JSON.stringify(NOTIFICATION_SETTINGS)),
    sessions: JSON.parse(JSON.stringify(SESSIONS)),
    passkeys: JSON.parse(JSON.stringify(PASSKEYS)),
    apiKeys: JSON.parse(JSON.stringify(API_KEYS)),
    authorizedApps: JSON.parse(JSON.stringify(AUTHORIZED_APPS)),
    _nextApiKeyId: 10,
    _nextPasskeyId: 10
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_entity(entities, **kwargs):
    for e in entities:
        if all(e.get(k) == v for k, v in kwargs.items()):
            return e
    raise ValueError(f"Entity not found: {kwargs}")


# ── solve functions ──────────────────────────────────────────────────

# Easy tasks

def solve_task_e1(state):
    """Switch the interface to dark mode."""
    state["preferences"]["interfaceTheme"] = "Dark"

def solve_task_e2(state):
    """Turn off the emoji conversion for text emoticons."""
    state["preferences"]["convertTextEmojis"] = False

def solve_task_e3(state):
    """Disable desktop notifications."""
    state["notificationSettings"]["desktop"]["enabled"] = False

def solve_task_e4(state):
    """Change the username to 'amorgan'."""
    state["currentUser"]["username"] = "amorgan"

def solve_task_e5(state):
    """Turn on auto-assign when creating issues."""
    state["preferences"]["autoAssignOnCreate"] = True

def solve_task_e6(state):
    """Stop receiving changelog notifications."""
    state["notificationSettings"]["receiveChangelogs"] = False

def solve_task_e7(state):
    """Set the default home view to My Issues."""
    state["preferences"]["defaultHomeView"] = "My Issues"

def solve_task_e8(state):
    """Remove the YubiKey passkey."""
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "YubiKey 5C NFC"]

def solve_task_e9(state):
    """Revoke the Zapier integration."""
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Zapier"]

def solve_task_e10(state):
    """Increase the font size to Large."""
    state["preferences"]["fontSize"] = "Large"

def solve_task_e11(state):
    """Disconnect the Figma account."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "Figma"]

def solve_task_e12(state):
    """Turn off the desktop app notification badge."""
    state["preferences"]["desktopNotificationBadge"] = False

def solve_task_e13(state):
    """Enable Slack notifications."""
    state["notificationSettings"]["slack"]["enabled"] = True

def solve_task_e14(state):
    """Revoke the Mobile App Testing API key."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] != "Mobile App Testing"]

def solve_task_e15(state):
    """Disable spell check."""
    state["preferences"]["enableSpellCheck"] = False

def solve_task_e16(state):
    """Set Sunday as the first day of the week."""
    state["preferences"]["firstDayOfWeek"] = "Sunday"

def solve_task_e17(state):
    """Enable the pointer cursor."""
    state["preferences"]["usePointerCursor"] = True

def solve_task_e18(state):
    """Turn off the open in desktop app setting."""
    state["preferences"]["openInDesktopApp"] = False

def solve_task_e19(state):
    """Opt in to product update communications."""
    state["notificationSettings"]["receiveProductUpdates"] = True

def solve_task_e20(state):
    """Stop showing full names."""
    state["preferences"]["displayFullNames"] = False

# Medium tasks

def solve_task_m1(state):
    """Update name to 'Jordan Rivera' and username to 'jrivera'."""
    state["currentUser"]["fullName"] = "Jordan Rivera"
    state["currentUser"]["username"] = "jrivera"

def solve_task_m2(state):
    """Revoke Firefox on Windows session."""
    state["sessions"] = [s for s in state["sessions"] if s["deviceName"] != "Firefox on Windows"]

def solve_task_m3(state):
    """Change email to 'alex.morgan@newcompany.com'."""
    state["currentUser"]["email"] = "alex.morgan@newcompany.com"

def solve_task_m4(state):
    """Create a new API key labeled 'Staging Environment'."""
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Staging Environment",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_m5(state):
    """Register a new passkey called 'Windows Hello'."""
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Windows Hello",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_m6(state):
    """Turn off email status changes, turn on comments."""
    state["notificationSettings"]["email"]["issueStatusChanged"] = False
    state["notificationSettings"]["email"]["issueCommented"] = True

def solve_task_m7(state):
    """Dark - Contrast theme, Small font."""
    state["preferences"]["interfaceTheme"] = "Dark - Contrast"
    state["preferences"]["fontSize"] = "Small"

def solve_task_m8(state):
    """Leave Side Project Labs workspace."""
    state["workspaces"] = [w for w in state["workspaces"] if w["name"] != "Side Project Labs"]

def solve_task_m9(state):
    """Disable mobile notifications."""
    state["notificationSettings"]["mobile"]["enabled"] = False

def solve_task_m10(state):
    """Git attachment format to 'Title and repository', auto-assign on started."""
    state["preferences"]["gitAttachmentFormat"] = "Title and repository"
    state["preferences"]["autoAssignOnStarted"] = True

def solve_task_m11(state):
    """Revoke Notion Integration and Linear Exporter."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] not in ("Notion Integration", "Linear Exporter")]

def solve_task_m12(state):
    """Disconnect GitLab."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"] if a["provider"] != "GitLab"]

def solve_task_m13(state):
    """Enable desktop cycle update notifications."""
    state["notificationSettings"]["desktop"]["cycleUpdated"] = True

def solve_task_m14(state):
    """Turn off delay low priority outside hours."""
    state["notificationSettings"]["email"]["delayLowPriorityOutsideHours"] = False

def solve_task_m15(state):
    """Stop auto-assign on git branch copy."""
    state["preferences"]["onGitBranchCopyAutoAssign"] = False

def solve_task_m16(state):
    """Revoke Data Export Script and Slack Bot Integration API keys."""
    state["apiKeys"] = [k for k in state["apiKeys"]
                        if k["label"] not in ("Data Export Script", "Slack Bot Integration")]

def solve_task_m17(state):
    """Stop sending urgent email notifications immediately."""
    state["notificationSettings"]["email"]["sendUrgentImmediately"] = False

def solve_task_m18(state):
    """Remove iPhone Face ID passkey."""
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "iPhone Face ID"]

def solve_task_m19(state):
    """Set home view to Inbox, first day to Wednesday."""
    state["preferences"]["defaultHomeView"] = "Inbox"
    state["preferences"]["firstDayOfWeek"] = "Wednesday"

def solve_task_m20(state):
    """Revoke the Linux session."""
    state["sessions"] = [s for s in state["sessions"] if s["deviceName"] != "Chrome on Linux"]

# Hard tasks

def solve_task_h1(state):
    """Light - Contrast theme, Small font, pointer cursor on, emoticons off."""
    state["preferences"]["interfaceTheme"] = "Light - Contrast"
    state["preferences"]["fontSize"] = "Small"
    state["preferences"]["usePointerCursor"] = True
    state["preferences"]["convertTextEmojis"] = False

def solve_task_h2(state):
    """Revoke all sessions except current."""
    state["sessions"] = [s for s in state["sessions"] if s.get("isCurrent", False)]

def solve_task_h3(state):
    """Disconnect GitHub and GitLab."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] not in ("GitHub", "GitLab")]

def solve_task_h4(state):
    """Disable all notification channels."""
    for channel in ("desktop", "mobile", "email", "slack"):
        state["notificationSettings"][channel]["enabled"] = False

def solve_task_h5(state):
    """Revoke all authorized apps."""
    state["authorizedApps"] = []

def solve_task_h6(state):
    """Change name to Sam Chen, username to schen, email to sam.chen@acmecorp.io."""
    state["currentUser"]["fullName"] = "Sam Chen"
    state["currentUser"]["username"] = "schen"
    state["currentUser"]["email"] = "sam.chen@acmecorp.io"

def solve_task_h7(state):
    """Disable git automations, change format."""
    state["preferences"]["onGitBranchCopyMoveToStarted"] = False
    state["preferences"]["onGitBranchCopyAutoAssign"] = False
    state["preferences"]["gitAttachmentFormat"] = "Title and repository"

def solve_task_h8(state):
    """Unsubscribe from all comms, disable email channel."""
    state["notificationSettings"]["receiveChangelogs"] = False
    state["notificationSettings"]["receiveDpaUpdates"] = False
    state["notificationSettings"]["receiveProductUpdates"] = False
    state["notificationSettings"]["email"]["enabled"] = False

def solve_task_h9(state):
    """Create 'GitHub Actions' API key, revoke 'CI/CD Pipeline'."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] != "CI/CD Pipeline"]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "GitHub Actions",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_h10(state):
    """Leave both non-admin workspaces."""
    state["workspaces"] = [w for w in state["workspaces"] if w["role"] == "Admin"]

def solve_task_h11(state):
    """Minimal workspace preferences."""
    state["preferences"]["interfaceTheme"] = "Dark"
    state["preferences"]["fontSize"] = "Small"
    state["preferences"]["defaultHomeView"] = "Inbox"
    state["preferences"]["displayFullNames"] = False
    state["preferences"]["convertTextEmojis"] = False
    state["preferences"]["openInDesktopApp"] = False

def solve_task_h12(state):
    """Remove all passkeys."""
    state["passkeys"] = []

def solve_task_h13(state):
    """Revoke all mobile device sessions."""
    state["sessions"] = [s for s in state["sessions"] if s.get("deviceType") != "mobile"]

def solve_task_h14(state):
    """Auto-assign on create and started, home view to Current cycle."""
    state["preferences"]["autoAssignOnCreate"] = True
    state["preferences"]["autoAssignOnStarted"] = True
    state["preferences"]["defaultHomeView"] = "Current cycle"

def solve_task_h15(state):
    """Disconnect Slack and Google, disable Slack notifications."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] not in ("Slack", "Google")]
    state["notificationSettings"]["slack"]["enabled"] = False

def solve_task_h16(state):
    """Revoke all API keys with expiration dates."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k.get("expiresAt") is None]

def solve_task_h17(state):
    """Enable all desktop notification types."""
    desktop = state["notificationSettings"]["desktop"]
    desktop["enabled"] = True
    desktop["issueAssigned"] = True
    desktop["issueStatusChanged"] = True
    desktop["issueCommented"] = True
    desktop["issueMentioned"] = True
    desktop["projectUpdated"] = True
    desktop["cycleUpdated"] = True

def solve_task_h18(state):
    """Revoke all OAuth apps with write permissions."""
    state["authorizedApps"] = [
        a for a in state["authorizedApps"]
        if not any("write" in p for p in a.get("permissions", []))
    ]

def solve_task_h19(state):
    """Turn off all desktop application settings."""
    state["preferences"]["openInDesktopApp"] = False
    state["preferences"]["desktopNotificationBadge"] = False
    state["preferences"]["enableSpellCheck"] = False

def solve_task_h20(state):
    """Revoke NY and Seattle sessions, add Security Key Backup passkey."""
    state["sessions"] = [s for s in state["sessions"]
                         if "New York" not in s.get("location", "")
                         and "Seattle" not in s.get("location", "")]
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Security Key Backup",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "cross-platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

# Hardening round 1 tasks (h21-h40)

def solve_task_h21(state):
    """Update email to Google account's email, disconnect Google."""
    state["currentUser"]["email"] = "alex.morgan@gmail.com"
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Google"]

def solve_task_h22(state):
    """Revoke non-California sessions, create 'West Coast Only' API key."""
    state["sessions"] = [s for s in state["sessions"] if ", CA," in s.get("location", "")]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "West Coast Only",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_h23(state):
    """Revoke least recently used API key and earliest authorized OAuth app."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] != "Mobile App Testing"]
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Zapier"]

def solve_task_h24(state):
    """Enable cycle updates for enabled channels (desktop, mobile, email)."""
    for channel in ("desktop", "mobile", "email"):
        state["notificationSettings"][channel]["cycleUpdated"] = True

def solve_task_h25(state):
    """Disconnect non-SCM accounts, unsubscribe from all comms."""
    scm = {"GitHub", "GitLab"}
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] in scm]
    state["notificationSettings"]["receiveChangelogs"] = False
    state["notificationSettings"]["receiveDpaUpdates"] = False
    state["notificationSettings"]["receiveProductUpdates"] = False

def solve_task_h26(state):
    """Revoke OAuth app with most permissions (Zapier), remove newest passkey (iPhone Face ID)."""
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Zapier"]
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "iPhone Face ID"]

def solve_task_h27(state):
    """Full lockdown: disable all channels, disconnect all accounts, revoke all apps."""
    for channel in ("desktop", "mobile", "email", "slack"):
        state["notificationSettings"][channel]["enabled"] = False
    state["connectedAccounts"] = []
    state["authorizedApps"] = []

def solve_task_h28(state):
    """Invert all email notification types."""
    email = state["notificationSettings"]["email"]
    for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                "issueMentioned", "projectUpdated", "cycleUpdated"):
        email[key] = not email[key]

def solve_task_h29(state):
    """Set username to email local part, disable full names."""
    email_addr = state["currentUser"]["email"]
    local_part = email_addr.split("@")[0]
    state["currentUser"]["username"] = local_part
    state["preferences"]["displayFullNames"] = False

def solve_task_h30(state):
    """Revoke non-current desktop sessions, disable desktop notifs, turn off desktop app prefs."""
    state["sessions"] = [s for s in state["sessions"]
                         if s.get("deviceType") != "desktop" or s.get("isCurrent")]
    state["notificationSettings"]["desktop"]["enabled"] = False
    state["preferences"]["openInDesktopApp"] = False
    state["preferences"]["desktopNotificationBadge"] = False
    state["preferences"]["enableSpellCheck"] = False

def solve_task_h31(state):
    """Revoke sessions with earliest and most recent sign-in (non-current)."""
    state["sessions"] = [s for s in state["sessions"]
                         if s["deviceName"] not in ("Edge on Windows", "Firefox on Windows")]

def solve_task_h32(state):
    """Revoke OAuth apps with read:teams, leave workspace with fewest members."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if "read:teams" not in a.get("permissions", [])]
    state["workspaces"] = [w for w in state["workspaces"]
                           if w["name"] != "Side Project Labs"]

def solve_task_h33(state):
    """Create API key labeled 'Admin' (Acme Corp role), enable both auto-assign."""
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Admin",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1
    state["preferences"]["autoAssignOnCreate"] = True
    state["preferences"]["autoAssignOnStarted"] = True

def solve_task_h34(state):
    """Enable Slack with all types, disable email channel."""
    slack = state["notificationSettings"]["slack"]
    slack["enabled"] = True
    for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                "issueMentioned", "projectUpdated", "cycleUpdated"):
        slack[key] = True
    state["notificationSettings"]["email"]["enabled"] = False

def solve_task_h35(state):
    """Disconnect account with different email domain (Google), set home to Favorited Views."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Google"]
    state["preferences"]["defaultHomeView"] = "Favorited Views"

def solve_task_h36(state):
    """Keep only most recently used API key (CI/CD Pipeline), revoke read-only OAuth apps."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k["label"] == "CI/CD Pipeline"]
    state["authorizedApps"] = [
        a for a in state["authorizedApps"]
        if any("write" in p for p in a.get("permissions", []))
    ]

def solve_task_h37(state):
    """All 4 channels enabled, only mentions type on."""
    for channel in ("desktop", "mobile", "email", "slack"):
        ch = state["notificationSettings"][channel]
        ch["enabled"] = True
        ch["issueAssigned"] = False
        ch["issueStatusChanged"] = False
        ch["issueCommented"] = False
        ch["issueMentioned"] = True
        ch["projectUpdated"] = False
        ch["cycleUpdated"] = False

def solve_task_h38(state):
    """Remove least used passkey (YubiKey), disconnect most recent SCM (GitLab), revoke Win10 session."""
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "YubiKey 5C NFC"]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "GitLab"]
    state["sessions"] = [s for s in state["sessions"] if "Windows 10" not in s.get("os", "")]

def solve_task_h39(state):
    """Maximum notifications: all channels, all types, all comms."""
    notif_types = ("issueAssigned", "issueStatusChanged", "issueCommented",
                   "issueMentioned", "projectUpdated", "cycleUpdated")
    for channel in ("desktop", "mobile", "email", "slack"):
        ch = state["notificationSettings"][channel]
        ch["enabled"] = True
        for key in notif_types:
            ch[key] = True
    state["notificationSettings"]["receiveChangelogs"] = True
    state["notificationSettings"]["receiveDpaUpdates"] = True
    state["notificationSettings"]["receiveProductUpdates"] = True

def solve_task_h40(state):
    """Revoke two most recently authorized OAuth apps, add passkey 'Acme Corp'."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] not in ("Screenful", "Marker.io")]
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Acme Corp",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1


# Hardening round 2 tasks (h41-h60)

def solve_task_h41(state):
    """Username = urlKey of most recently joined workspace, leave it."""
    state["currentUser"]["username"] = "osc"
    state["workspaces"] = [w for w in state["workspaces"]
                           if w["name"] != "Open Source Collective"]

def solve_task_h42(state):
    """Create API key named after most-perms OAuth app (Zapier), revoke it."""
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Zapier",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1
    state["authorizedApps"] = [a for a in state["authorizedApps"] if a["name"] != "Zapier"]

def solve_task_h43(state):
    """Revoke non-Apple-OS sessions, remove cross-platform passkey."""
    apple_keywords = ("macOS", "iOS", "iPadOS")
    state["sessions"] = [s for s in state["sessions"]
                         if any(a in s.get("os", "") for a in apple_keywords)]
    state["passkeys"] = [p for p in state["passkeys"]
                         if p.get("credentialType") != "cross-platform"]

def solve_task_h44(state):
    """Disable all types in enabled channels, leave disabled channels."""
    notif_types = ("issueAssigned", "issueStatusChanged", "issueCommented",
                   "issueMentioned", "projectUpdated", "cycleUpdated")
    for channel in ("desktop", "mobile", "email"):
        for key in notif_types:
            state["notificationSettings"][channel][key] = False

def solve_task_h45(state):
    """Revoke Texas and New York sessions, create passkey 'San Francisco'."""
    state["sessions"] = [s for s in state["sessions"]
                         if "Austin" not in s.get("location", "")
                         and "New York" not in s.get("location", "")]
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "San Francisco",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_h46(state):
    """Add passkey 'Google' (longest connected), remove YubiKey (least recently used)."""
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Google",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "YubiKey 5C NFC"]

def solve_task_h47(state):
    """Revoke pre-2026 sessions, disable mobile, add 'Post-Cleanup Key'."""
    state["sessions"] = [s for s in state["sessions"]
                         if s.get("signedInAt", "") >= "2026-01-01" or s.get("isCurrent")]
    state["notificationSettings"]["mobile"]["enabled"] = False
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Post-Cleanup Key",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_h48(state):
    """Disconnect Figma (fewest scopes), revoke Linear Exporter (least accessed), create API key 'Figma'."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Figma"]
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] != "Linear Exporter"]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Figma",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_h49(state):
    """Invert desktop and mobile notification types."""
    for channel in ("desktop", "mobile"):
        ch = state["notificationSettings"][channel]
        for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                    "issueMentioned", "projectUpdated", "cycleUpdated"):
            ch[key] = not ch[key]

def solve_task_h50(state):
    """Revoke pre-2026 API keys, create 'Primary' and 'Backup'."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k.get("createdAt", "") >= "2026-01-01"]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    for label in ("Primary", "Backup"):
        state["apiKeys"].append({
            "id": f"apikey_{key_id:02d}",
            "label": label,
            "keyPrefix": "lin_api_test",
            "createdAt": now,
            "lastUsedAt": None,
            "expiresAt": None
        })
        key_id += 1
    state["_nextApiKeyId"] = key_id

def solve_task_h51(state):
    """Set email notification types to match desktop types."""
    desktop = state["notificationSettings"]["desktop"]
    email = state["notificationSettings"]["email"]
    for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                "issueMentioned", "projectUpdated", "cycleUpdated"):
        email[key] = desktop[key]

def solve_task_h52(state):
    """Revoke most recently signed-in non-current session and most recently created API key."""
    state["sessions"] = [s for s in state["sessions"]
                         if s["deviceName"] != "Firefox on Windows"]
    state["apiKeys"] = [k for k in state["apiKeys"]
                        if k["label"] != "Mobile App Testing"]

def solve_task_h53(state):
    """Revoke OAuth with <5 perms, disconnect same-domain accounts."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if len(a.get("permissions", [])) >= 5]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if "acmecorp.io" not in a.get("accountEmail", "")]

def solve_task_h54(state):
    """Revoke no-expiry API keys, create 'Replacement', enable both auto-assigns."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k.get("expiresAt") is not None]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Replacement",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1
    state["preferences"]["autoAssignOnCreate"] = True
    state["preferences"]["autoAssignOnStarted"] = True

def solve_task_h55(state):
    """Revoke sessions not from same city as current session (San Francisco)."""
    state["sessions"] = [s for s in state["sessions"]
                         if "San Francisco" in s.get("location", "")]

def solve_task_h56(state):
    """Enable Slack with opposite types of email channel."""
    email = state["notificationSettings"]["email"]
    slack = state["notificationSettings"]["slack"]
    slack["enabled"] = True
    for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                "issueMentioned", "projectUpdated", "cycleUpdated"):
        slack[key] = not email[key]

def solve_task_h57(state):
    """Full name = 'Alex Morgan (Admin)', home view = All issues, display full names off."""
    state["currentUser"]["fullName"] = "Alex Morgan (Admin)"
    state["preferences"]["defaultHomeView"] = "All issues"
    state["preferences"]["displayFullNames"] = False

def solve_task_h58(state):
    """Remove earliest passkey, revoke earliest OAuth, disconnect newest account."""
    state["passkeys"] = [p for p in state["passkeys"]
                         if p["name"] != "MacBook Pro Touch ID"]
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] != "Zapier"]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Figma"]

def solve_task_h59(state):
    """Revoke tablet sessions, disconnect >2 scopes accounts, disable comms."""
    state["sessions"] = [s for s in state["sessions"]
                         if s.get("deviceType") != "tablet"]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if len(a.get("scopes", [])) <= 2]
    state["notificationSettings"]["receiveChangelogs"] = False
    state["notificationSettings"]["receiveDpaUpdates"] = False
    state["notificationSettings"]["receiveProductUpdates"] = False

def solve_task_h60(state):
    """Invert channel enabled states, leave types unchanged."""
    for channel in ("desktop", "mobile", "email", "slack"):
        ch = state["notificationSettings"][channel]
        ch["enabled"] = not ch["enabled"]


# Hardening round 3 tasks (h61-h80)

def solve_task_h61(state):
    """Username = URL key of most-member workspace, firstDayOfWeek = sign-in day."""
    state["currentUser"]["username"] = "osc"
    state["preferences"]["firstDayOfWeek"] = "Sunday"

def solve_task_h62(state):
    """Revoke OAuth apps with perm count = same-domain connected account count."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if len(a.get("permissions", [])) != 4]

def solve_task_h63(state):
    """Revoke API key containing provider name, disconnect that provider."""
    state["apiKeys"] = [k for k in state["apiKeys"]
                        if k["label"] != "Slack Bot Integration"]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Slack"]

def solve_task_h64(state):
    """Revoke session with lowest browser version, create API key with city."""
    state["sessions"] = [s for s in state["sessions"]
                         if s["deviceName"] != "Linear Desktop on macOS"]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "San Francisco",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1

def solve_task_h65(state):
    """Revoke read-only OAuth apps, create API key per revoked app."""
    read_only = ["Notion Integration", "Linear Exporter", "Screenful"]
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] not in read_only]
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    for label in read_only:
        state["apiKeys"].append({
            "id": f"apikey_{key_id:02d}",
            "label": label,
            "keyPrefix": "lin_api_test",
            "createdAt": now,
            "lastUsedAt": None,
            "expiresAt": None
        })
        key_id += 1
    state["_nextApiKeyId"] = key_id

def solve_task_h66(state):
    """Conditional channel toggle: enabled->disable+types on, disabled->enable+types off."""
    types = ("issueAssigned", "issueStatusChanged", "issueCommented",
             "issueMentioned", "projectUpdated", "cycleUpdated")
    for channel in ("desktop", "mobile", "email", "slack"):
        ch = state["notificationSettings"][channel]
        was_enabled = ch["enabled"]
        ch["enabled"] = not was_enabled
        for t in types:
            ch[t] = was_enabled

def solve_task_h67(state):
    """Disconnect account linked same day as account creation, home to last alphabetically."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Google"]
    state["preferences"]["defaultHomeView"] = "My Issues"

def solve_task_h68(state):
    """Count passkeys (3), revoke 3 most recently authorized OAuth apps."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] not in ("Screenful", "Marker.io", "Linear Exporter")]

def solve_task_h69(state):
    """Revoke weekday sessions, passkey named after account creation day."""
    weekday_sessions = [
        "Safari on iPhone", "Linear Desktop on macOS", "Firefox on Windows",
        "Chrome on Linux", "Safari on iPad", "Edge on Windows"
    ]
    state["sessions"] = [s for s in state["sessions"]
                         if s["deviceName"] not in weekday_sessions]
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Saturday",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_h70(state):
    """Revoke odd-month OAuth apps, disconnect even-month connected accounts."""
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] == "Marker.io"]
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] == "Figma"]

def solve_task_h71(state):
    """Most-types channel -> mentions-only; fewest-types channel -> all-on."""
    types = ("issueAssigned", "issueStatusChanged", "issueCommented",
             "issueMentioned", "projectUpdated", "cycleUpdated")
    desktop = state["notificationSettings"]["desktop"]
    for t in types:
        desktop[t] = (t == "issueMentioned")
    email = state["notificationSettings"]["email"]
    for t in types:
        email[t] = True

def solve_task_h72(state):
    """Create 'Admin-6' API key, revoke OAuth with read+write issues."""
    key_id = state.get("_nextApiKeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["apiKeys"].append({
        "id": f"apikey_{key_id:02d}",
        "label": "Admin-6",
        "keyPrefix": "lin_api_test",
        "createdAt": now,
        "lastUsedAt": None,
        "expiresAt": None
    })
    state["_nextApiKeyId"] = key_id + 1
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] not in ("Raycast", "Zapier", "Marker.io")]

def solve_task_h73(state):
    """Disconnect email-address accounts, revoke OAuth with period in name."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] not in ("Figma", "Google")]
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] != "Marker.io"]

def solve_task_h74(state):
    """Display name = capitalized username, home = Current cycle, both auto-assigns."""
    state["currentUser"]["fullName"] = "Alexmorgan"
    state["preferences"]["defaultHomeView"] = "Current cycle"
    state["preferences"]["autoAssignOnCreate"] = True
    state["preferences"]["autoAssignOnStarted"] = True

def solve_task_h75(state):
    """Revoke API keys from 2025 (same year as passkeys), remove newest passkey."""
    state["apiKeys"] = [k for k in state["apiKeys"] if k.get("createdAt", "") >= "2026-01-01"]
    state["passkeys"] = [p for p in state["passkeys"] if p["name"] != "iPhone Face ID"]

def solve_task_h76(state):
    """All channels enabled; desktop+email types off; mobile+slack types on."""
    types = ("issueAssigned", "issueStatusChanged", "issueCommented",
             "issueMentioned", "projectUpdated", "cycleUpdated")
    for channel in ("desktop", "mobile", "email", "slack"):
        state["notificationSettings"][channel]["enabled"] = True
    for channel in ("desktop", "email"):
        for t in types:
            state["notificationSettings"][channel][t] = False
    for channel in ("mobile", "slack"):
        for t in types:
            state["notificationSettings"][channel][t] = True

def solve_task_h77(state):
    """Revoke earliest API key, passkey with its label."""
    state["apiKeys"] = [k for k in state["apiKeys"]
                        if k["label"] != "Monitoring Dashboard"]
    pk_id = state.get("_nextPasskeyId", 10)
    now = "2026-03-06T12:00:00.000Z"
    state["passkeys"].append({
        "id": f"pk_{pk_id:02d}",
        "name": "Monitoring Dashboard",
        "createdAt": now,
        "lastUsedAt": now,
        "credentialType": "platform"
    })
    state["_nextPasskeyId"] = pk_id + 1

def solve_task_h78(state):
    """Conditional: >3 types -> comments+mentions; <=3 -> all on. Skip disabled."""
    types = ("issueAssigned", "issueStatusChanged", "issueCommented",
             "issueMentioned", "projectUpdated", "cycleUpdated")
    desktop = state["notificationSettings"]["desktop"]
    for t in types:
        desktop[t] = t in ("issueCommented", "issueMentioned")
    mobile = state["notificationSettings"]["mobile"]
    for t in types:
        mobile[t] = t in ("issueCommented", "issueMentioned")
    email = state["notificationSettings"]["email"]
    for t in types:
        email[t] = True

def solve_task_h79(state):
    """Disconnect write-scope accounts, revoke most-recent OAuth, Light-Contrast."""
    state["connectedAccounts"] = [a for a in state["connectedAccounts"]
                                   if a["provider"] != "Slack"]
    state["authorizedApps"] = [a for a in state["authorizedApps"]
                                if a["name"] != "Raycast"]
    state["preferences"]["interfaceTheme"] = "Light - Contrast"

def solve_task_h80(state):
    """Security audit: revoke old sessions, unused passkeys, unused API keys."""
    state["sessions"] = [s for s in state["sessions"]
                         if s.get("signedInAt", "") >= "2025-12-06" or s.get("isCurrent")]
    state["passkeys"] = [p for p in state["passkeys"]
                         if p.get("lastUsedAt", "") >= "2026-02-27"]
    state["apiKeys"] = [k for k in state["apiKeys"]
                        if k.get("lastUsedAt", "") >= "2026-02-27"]


SOLVERS = {}
for _difficulty in ("e", "m", "h"):
    for _i in range(1, 81):
        _task_id = f"task_{_difficulty}{_i}"
        _fn_name = f"solve_task_{_difficulty}{_i}"
        if _fn_name in globals():
            SOLVERS[_task_id] = globals()[_fn_name]


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    port = start
    while port < start + 200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+200}")


def start_server(port):
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/", timeout=1)
            return proc
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.2)
    proc.kill()
    raise RuntimeError(f"Server failed to start on port {port}")


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


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

        # 3. Apply the solve function
        solver(state)

        # 4. Write solved state back
        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        # 5. Run the verifier
        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message

    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    proc = start_server(port)
    server_url = f"http://localhost:{port}"
    results = []
    try:
        seed_server(server_url, seed_state)
        for task in tasks:
            result = run_single_task(task, server_url)
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    results = []

    def worker_fn(task, port):
        proc = start_server(port)
        server_url = f"http://localhost:{port}"
        try:
            seed_server(server_url, seed_state)
            return run_single_task(task, server_url)
        finally:
            stop_server(proc)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for i, task in enumerate(tasks):
            port = base_port + i
            future = executor.submit(worker_fn, task, port)
            futures[future] = task["id"]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")

    return results


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Linear Account Settings real-task sanity check")
    parser.add_argument("--task-id", type=str, help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--port", type=int, default=9600, help="Base port for servers")
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
