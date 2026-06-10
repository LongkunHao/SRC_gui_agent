#!/usr/bin/env python3
"""
Generate the main results figures for the blog post:
  1. Grouped bar chart — per-app + overall success rates for 3 models
  2. Table data — avg steps & time per model (printed to stdout + saved as CSV)
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
OUT_DIR   = REPO / "analysis" / "output"
DPI = 300

# ── Apps (10 included, matching reports) ──────────────────────────────────────

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

# Short display names for the x-axis
APP_LABELS = {
    "elation-clinical-records": "Elation\nClinical",
    "elation-prescriptions": "Elation\nPrescription",
    "gitlab-plan-and-track": "GitLab\nPlan & Track",
    "gmail": "Gmail",
    "gmail-accounts-and-contacts": "Gmail\nAcct & Contact",
    "handshake-career-exploration": "Handshake",
    "linear-account-settings": "Linear\nAcct Mgmt",
    "paypal-my-wallet": "PayPal\nWallet",
    "superhuman-general": "Super-\nhuman",
    "xero-invoicing": "Xero\nInvoicing",
}

# Gemini result folders from the final report
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

# Colors from the style guide multi-line cycle
COLOR_GEMINI = "#77B1F2"   # soft blue (primary)
COLOR_QWEN   = "#E8A85C"   # muted orange (alt)
COLOR_KIMI   = "#8BC7A3"   # muted green

# ── Data loading ──────────────────────────────────────────────────────────────

GEMINI_APP_DIR = {
    "linear-account-settings": "linear-account-settings-v2",
}

def load_gemini_results(app):
    folder = GEMINI_FOLDERS[app]
    dir_name = GEMINI_APP_DIR.get(app, app)
    path = S3_GEMINI / dir_name / folder / "results.json"
    with open(path) as f:
        return json.load(f)

def load_kimi_results(app):
    path = S3_KIMI / app / "results.json"
    with open(path) as f:
        return json.load(f)

def load_qwen_results(app):
    path = S3_QWEN / app / "results.json"
    with open(path) as f:
        return json.load(f)

def extract_stats(data):
    """Return (pass_rate, avg_steps, avg_elapsed, tasks) from results.json."""
    tasks = data["tasks"]
    pr = data["pass_rate"]
    steps = [t["steps"] for t in tasks if t["steps"] >= 0]
    elapsed = [t["elapsed"] for t in tasks if t["elapsed"] > 0]
    return pr, np.mean(steps) if steps else 0, np.mean(elapsed) if elapsed else 0, tasks


# ── Figure 1: Grouped bar chart ──────────────────────────────────────────────

def plot_bar_chart():
    gemini_sr, kimi_sr, qwen_sr = [], [], []
    gemini_steps, kimi_steps, qwen_steps = [], [], []
    gemini_time, kimi_time, qwen_time = [], [], []
    gemini_all_tasks, kimi_all_tasks, qwen_all_tasks = [], [], []

    for app in APPS:
        g = extract_stats(load_gemini_results(app))
        k = extract_stats(load_kimi_results(app))
        q = extract_stats(load_qwen_results(app))
        gemini_sr.append(g[0]); kimi_sr.append(k[0]); qwen_sr.append(q[0])
        gemini_steps.append(g[1]); kimi_steps.append(k[1]); qwen_steps.append(q[1])
        gemini_time.append(g[2]); kimi_time.append(k[2]); qwen_time.append(q[2])
        gemini_all_tasks.extend(g[3]); kimi_all_tasks.extend(k[3]); qwen_all_tasks.extend(q[3])

    # Add overall as the first group
    labels = ["Overall"] + [APP_LABELS[a] for a in APPS]
    gemini_vals = [sum(t["passed"] for t in gemini_all_tasks) / len(gemini_all_tasks) * 100] + gemini_sr
    kimi_vals   = [sum(t["passed"] for t in kimi_all_tasks)   / len(kimi_all_tasks) * 100]   + kimi_sr
    qwen_vals   = [sum(t["passed"] for t in qwen_all_tasks)   / len(qwen_all_tasks) * 100]   + qwen_sr

    n = len(labels)
    x = np.arange(n)
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 3.5))

    bars_g = ax.bar(x - width, gemini_vals, width, color=COLOR_GEMINI,
                    edgecolor='white', linewidth=0.5, zorder=3,
                    label='Gemini 3 Flash w/ Browser Use')
    bars_q = ax.bar(x,         qwen_vals,   width, color=COLOR_QWEN,
                    edgecolor='white', linewidth=0.5, zorder=3,
                    label='Qwen 3.5 Plus')
    bars_k = ax.bar(x + width, kimi_vals,   width, color=COLOR_KIMI,
                    edgecolor='white', linewidth=0.5, zorder=3,
                    label='Kimi K2.5')

    # Value labels above bars
    for bars in [bars_g, bars_q, bars_k]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                    f'{h:.0f}', ha='center', va='bottom', fontsize=9,
                    color='#333')

    ax.set_ylabel('Success Rate (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, ha='right', rotation=20)
    ax.set_ylim(0, 118)

    # Shaded background behind "Overall" group (first position)
    ax.axvspan(-0.5, 0.5, color='#e8e8e8', zorder=0)

    ax.legend(frameon=True, framealpha=0.9, edgecolor='#DDD',
              loc='upper right', ncol=3)

    ax.set_title('Real-Task Success Rate by App and Model')

    plt.tight_layout()
    out = OUT_DIR / "fig_main_bar_chart.png"
    fig.savefig(out, dpi=DPI, bbox_inches='tight')
    print(f"Saved: {out}")
    plt.close(fig)

    # Return aggregated step/time data for the table
    return {
        "gemini": (gemini_all_tasks, gemini_steps, gemini_time),
        "kimi":   (kimi_all_tasks, kimi_steps, kimi_time),
        "qwen":   (qwen_all_tasks, qwen_steps, qwen_time),
    }


# ── Table: Steps and time ────────────────────────────────────────────────────

def print_table(data):
    print("\n=== Steps & Time Summary ===\n")
    header = f"{'Model':<20} {'Avg Steps':>10} {'Med Steps':>10} {'Avg Time (s)':>14} {'Med Time (s)':>14}"
    print(header)
    print("-" * len(header))

    rows = []
    for model_name, display_name in [("gemini", "Gemini 3 Flash w/ Browser Use"), ("qwen", "Qwen 3.5 Plus"), ("kimi", "Kimi K2.5")]:
        all_tasks, _, _ = data[model_name]
        steps = [t["steps"] for t in all_tasks if t["steps"] >= 0]
        elapsed = [t["elapsed"] for t in all_tasks if t["elapsed"] > 0]
        avg_s = np.mean(steps); med_s = np.median(steps)
        avg_e = np.mean(elapsed); med_e = np.median(elapsed)
        print(f"{display_name:<20} {avg_s:>10.1f} {med_s:>10.1f} {avg_e:>14.1f} {med_e:>14.1f}")
        rows.append({
            "model": display_name,
            "avg_steps": round(avg_s, 1),
            "median_steps": round(med_s, 1),
            "avg_time_s": round(avg_e, 1),
            "median_time_s": round(med_e, 1),
        })

    # Also break down by pass/fail
    print("\n=== Steps & Time by Outcome ===\n")
    for model_name, display_name in [("gemini", "Gemini 3 Flash w/ Browser Use"), ("qwen", "Qwen 3.5 Plus"), ("kimi", "Kimi K2.5")]:
        all_tasks, _, _ = data[model_name]
        for outcome, label in [(True, "Pass"), (False, "Fail")]:
            subset = [t for t in all_tasks if t["passed"] == outcome]
            steps = [t["steps"] for t in subset if t["steps"] >= 0]
            elapsed = [t["elapsed"] for t in subset if t["elapsed"] > 0]
            if steps:
                print(f"  {display_name} ({label}): steps={np.mean(steps):.1f} avg / {np.median(steps):.0f} med, "
                      f"time={np.mean(elapsed):.1f}s avg / {np.median(elapsed):.1f}s med  (n={len(subset)})")

    # Save as JSON for easy table generation
    out = OUT_DIR / "table_steps_time.json"
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nSaved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = plot_bar_chart()
    print_table(data)
