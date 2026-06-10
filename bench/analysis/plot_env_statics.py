#!/usr/bin/env python3
"""
Generate figures for the "Environment Statics" section of the blog post:
  1. A styled table figure showing per-app statistics
  2. A horizontal stacked bar chart showing task difficulty breakdown per app
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

REPO = Path("/home/ubuntu/mirror-mirror")
S3_GEMINI = REPO / "analysis" / "s3_results"
S3_KIMI   = REPO / "analysis" / "s3_results_kimi"
S3_QWEN   = REPO / "analysis" / "s3_results_qwen"
OUT_DIR   = REPO / "blog" / "figures"
DPI = 300

# ── Apps ──────────────────────────────────────────────────────────────────────

APPS = [
    "elation-clinical-records",
    "elation-prescriptions",
    "gitlab-plan-and-track",
    "gmail",
    "gmail-accounts-and-contacts",
    "handshake-career-exploration",
    "linear-account-settings",
    "paypal-my-wallet",
    "superhuman-general",
    "xero-invoicing",
]

# Display names (anonymized per content.md: "dont show the actual app like gitlab")
APP_DISPLAY = {
    "elation-clinical-records":     "Clinical Records",
    "elation-prescriptions":        "Prescriptions",
    "gitlab-plan-and-track":        "Plan & Track",
    "gmail":                        "Email",
    "gmail-accounts-and-contacts":  "Accts & Contacts",
    "handshake-career-exploration": "Career Explore",
    "linear-account-settings":      "Account Settings",
    "paypal-my-wallet":             "My Wallet",
    "superhuman-general":           "Email Client",
    "xero-invoicing":               "Invoicing",
}

APP_DOMAIN = {
    "elation-clinical-records":     "Healthcare",
    "elation-prescriptions":        "Healthcare",
    "gitlab-plan-and-track":        "DevOps",
    "gmail":                        "Productivity",
    "gmail-accounts-and-contacts":  "Productivity",
    "handshake-career-exploration": "Careers",
    "linear-account-settings":      "Project Mgmt",
    "paypal-my-wallet":             "Finance",
    "superhuman-general":           "Productivity",
    "xero-invoicing":               "Finance",
}

APP_SOURCE = {
    "elation-clinical-records":     "Elation EHR",
    "elation-prescriptions":        "Elation EHR",
    "gitlab-plan-and-track":        "GitLab",
    "gmail":                        "Gmail",
    "gmail-accounts-and-contacts":  "Gmail",
    "handshake-career-exploration": "Handshake",
    "linear-account-settings":      "Linear",
    "paypal-my-wallet":             "PayPal",
    "superhuman-general":           "Superhuman",
    "xero-invoicing":               "Xero",
}

GEMINI_FOLDERS = {
    "elation-clinical-records": "gemini_20260308_171406_p5_parallel",
    "elation-prescriptions": "gemini_20260308_045634_p5_parallel",
    "gitlab-plan-and-track": "gemini_20260301_163233_parallel",
    "gmail": "gemini_20260226_184951_real-tasks_parallel",
    "gmail-accounts-and-contacts": "gemini_20260308_124645_p5_parallel",
    "handshake-career-exploration": "gemini_20260308_140355_p5_parallel",
    "linear-account-settings": "gemini_20260306_084059_parallel",
    "paypal-my-wallet": "gemini_20260308_123918_p5_parallel",
    "superhuman-general": "gemini_20260308_154224_p5_parallel",
    "xero-invoicing": "gemini_20260306_073311_parallel",
}
GEMINI_APP_DIR = {"linear-account-settings": "linear-account-settings-v2"}

# ── Style (from FIGURE_STYLE_GUIDE.md) ───────────────────────────────────────

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 9,
    'axes.titlesize': 9,
    'axes.titleweight': 'normal',
    'axes.titlepad': 10,
    'axes.labelsize': 9,
    'axes.labelpad': 6,
    'axes.linewidth': 0.6,
    'axes.grid': False,
    'axes.spines.top': True,
    'axes.spines.right': True,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'figure.dpi': 100,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.08,
})

# Colors from style guide
COLOR_EASY     = "#8BC7A3"  # muted green
COLOR_MEDIUM   = "#F2CB6C"  # muted amber
COLOR_HARD_OG  = "#E8956A"  # muted orange — original hard
COLOR_HARDENED = "#A68BBF"  # muted purple — hardened
COLOR_BLUE     = "#77B1F2"  # soft blue
COLOR_RED      = "#F08D8D"  # soft red

# ── Data loading ──────────────────────────────────────────────────────────────

def get_passed_ids(path):
    try:
        data = json.load(open(path))
        return {t["task_id"] for t in data["tasks"] if t["passed"]}
    except Exception:
        return set()


def collect_data():
    rows = []
    for app in APPS:
        tasks = json.load(open(REPO / "apps" / app / "real-tasks.json"))
        n_total = len(tasks)

        # Difficulty breakdown
        n_easy = sum(1 for t in tasks if t["difficulty"] == "easy")
        n_medium = sum(1 for t in tasks if t["difficulty"] == "medium")
        n_hard = sum(1 for t in tasks if t["difficulty"] == "hard")

        # Split hard into original (h1-h8) and hardened (h9+)
        hard_tasks = [t for t in tasks if t["difficulty"] == "hard"]
        n_orig_hard = sum(1 for t in hard_tasks
                         if int(t["id"].replace("task_h", "")) <= 8)
        n_hardened = n_hard - n_orig_hard

        # Verified tasks (passed by at least one agent)
        gdir = GEMINI_APP_DIR.get(app, app)
        g = get_passed_ids(S3_GEMINI / gdir / GEMINI_FOLDERS[app] / "results.json")
        k = get_passed_ids(S3_KIMI / app / "results.json")
        q = get_passed_ids(S3_QWEN / app / "results.json")
        verified = len(g | k | q)

        rows.append({
            "app": app,
            "display": APP_DISPLAY[app],
            "domain": APP_DOMAIN[app],
            "source": APP_SOURCE[app],
            "total": n_total,
            "easy": n_easy,
            "medium": n_medium,
            "orig_hard": n_orig_hard,
            "hardened": n_hardened,
            "verified": verified,
        })
    return rows


# ── Figure 1: Table figure ───────────────────────────────────────────────────

def plot_table(rows):
    """Render a styled table as a figure."""
    col_labels = [
        "Environment", "Domain", "Source", "Tasks",
        "Easy", "Med", "Hard", "Hardened", "Verified"
    ]

    cell_text = []
    for r in rows:
        cell_text.append([
            r["display"],
            r["domain"],
            r["source"],
            str(r["total"]),
            str(r["easy"]),
            str(r["medium"]),
            str(r["orig_hard"]),
            str(r["hardened"]),
            f'{r["verified"]}/{r["total"]}',
        ])

    # Totals row
    totals = {k: sum(r[k] for r in rows) for k in
              ["total", "easy", "medium", "orig_hard", "hardened", "verified"]}
    cell_text.append([
        "Total", "", f"{len(rows)} apps",
        str(totals["total"]),
        str(totals["easy"]),
        str(totals["medium"]),
        str(totals["orig_hard"]),
        str(totals["hardened"]),
        f'{totals["verified"]}/{totals["total"]}',
    ])

    n_rows = len(cell_text)
    n_cols = len(col_labels)

    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.axis("off")

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8.5)

    # Style header
    for j in range(n_cols):
        cell = table[0, j]
        cell.set_facecolor("#4a7ec2")
        cell.set_text_props(color="white", fontweight="bold", fontsize=8.5)
        cell.set_edgecolor("white")
        cell.set_linewidth(0.5)

    # Style data rows
    for i in range(1, n_rows + 1):
        is_total = (i == n_rows)
        for j in range(n_cols):
            cell = table[i, j]
            cell.set_edgecolor("#DDD")
            cell.set_linewidth(0.5)
            if is_total:
                cell.set_facecolor("#e8edf4")
                cell.set_text_props(fontweight="bold", fontsize=8.5)
            elif i % 2 == 0:
                cell.set_facecolor("#f7f9fc")
            else:
                cell.set_facecolor("white")

    # Left-align text columns
    for i in range(n_rows + 1):
        for j in [0, 1, 2]:
            table[i, j].set_text_props(ha="left")
            table[i, j]._loc = "left"

    # Adjust column widths
    col_widths = [0.15, 0.11, 0.11, 0.06, 0.05, 0.05, 0.05, 0.08, 0.09]
    for j, w in enumerate(col_widths):
        for i in range(n_rows + 1):
            table[i, j].set_width(w)

    # Row height
    for i in range(n_rows + 1):
        for j in range(n_cols):
            table[i, j].set_height(0.06)

    ax.set_title("Generated Environment Statistics", pad=12)

    out = OUT_DIR / "fig_env_statics_table.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ── Figure 2: Horizontal stacked bar — task composition per app ──────────────

def plot_task_composition(rows):
    """Stacked horizontal bar showing easy/medium/hard/hardened per app."""
    labels = [r["display"] for r in rows]
    easy = [r["easy"] for r in rows]
    medium = [r["medium"] for r in rows]
    orig_hard = [r["orig_hard"] for r in rows]
    hardened = [r["hardened"] for r in rows]

    y = np.arange(len(labels))
    bar_h = 0.55

    fig, ax = plt.subplots(figsize=(6, 3.8))

    # Stack bars left to right
    b1 = ax.barh(y, easy, bar_h, color=COLOR_EASY, edgecolor="white",
                 linewidth=0.5, label="Easy")
    left = np.array(easy, dtype=float)

    b2 = ax.barh(y, medium, bar_h, left=left, color=COLOR_MEDIUM,
                 edgecolor="white", linewidth=0.5, label="Medium")
    left += np.array(medium, dtype=float)

    b3 = ax.barh(y, orig_hard, bar_h, left=left, color=COLOR_HARD_OG,
                 edgecolor="white", linewidth=0.5, label="Hard (Original)")
    left += np.array(orig_hard, dtype=float)

    b4 = ax.barh(y, hardened, bar_h, left=left, color=COLOR_HARDENED,
                 edgecolor="white", linewidth=0.5, label="Hard (Hardened)")
    left += np.array(hardened, dtype=float)

    # Total labels at right end of bars
    for i, total in enumerate(left):
        ax.text(total + 3, i, str(int(total)), va="center", ha="left",
                fontsize=8.5, color="#333")

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Number of Tasks")
    ax.set_title("Task Composition by Environment")
    ax.set_xlim(0, max(left) + 30)
    ax.invert_yaxis()

    ax.legend(frameon=True, framealpha=0.9, edgecolor="#DDD",
              loc="upper right", ncol=1, fontsize=8.5)

    plt.tight_layout()
    out = OUT_DIR / "fig_env_task_composition.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ── Figure 3: Verified vs unverified tasks per app ──────────────────────────

def plot_verified(rows):
    """Grouped bar showing verified vs total tasks, sorted by verification rate."""
    # Sort by verification rate descending
    sorted_rows = sorted(rows, key=lambda r: r["verified"] / r["total"], reverse=True)

    labels = [r["display"] for r in sorted_rows]
    verified = [r["verified"] for r in sorted_rows]
    total = [r["total"] for r in sorted_rows]
    unverified = [t - v for t, v in zip(total, verified)]
    rates = [v / t * 100 for v, t in zip(verified, total)]

    x = np.arange(len(labels))
    width = 0.55

    fig, ax = plt.subplots(figsize=(6, 3.5))

    ax.bar(x, verified, width, color=COLOR_BLUE, edgecolor="white",
           linewidth=0.5, label="Verified", zorder=3)
    ax.bar(x, unverified, width, bottom=verified, color=COLOR_RED,
           edgecolor="white", linewidth=0.5, label="Unverified", zorder=3,
           alpha=0.6)

    # Rate labels above bars
    for i, (v, t, rate) in enumerate(zip(verified, total, rates)):
        ax.text(i, t + 2, f"{rate:.0f}%", ha="center", va="bottom",
                fontsize=8.5, color="#333")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("Number of Tasks")
    ax.set_title("Task Verification Rate by Environment")
    ax.set_ylim(0, max(total) + 20)

    ax.legend(frameon=True, framealpha=0.9, edgecolor="#DDD",
              loc="upper right")

    plt.tight_layout()
    out = OUT_DIR / "fig_env_verified_tasks.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = collect_data()
    plot_table(rows)
    plot_task_composition(rows)
    plot_verified(rows)

    # Print summary
    total_tasks = sum(r["total"] for r in rows)
    total_verified = sum(r["verified"] for r in rows)
    print(f"\nSummary: {len(rows)} apps, {total_tasks} tasks, "
          f"{total_verified} verified ({total_verified/total_tasks*100:.1f}%)")
