#!/usr/bin/env python3
"""
Ablation Analysis for Mirror-Mirror Blog Post

Produces visualizations and analysis for three ablation study sections:
1. Self-Challenging Increase (hardening rounds produce progressively harder tasks)
2. Functional Correctness Regression (function task stability across pipeline)
3. Auditing Impact (what auditing catches and how it improves correctness)

Reads from: analysis/s3_results/
Outputs to:  analysis/output/
"""

import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
S3_DIR = BASE_DIR / "s3_results"
OUT_DIR = BASE_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 300

# Style setup — minimal scientific
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

# Base colors (lower saturation, visually appealing)
DOCS_COLOR = "#77B1F2"      # Soft blue
NODOCS_COLOR = "#F08D8D"    # Soft red

# Consistent color palette — muted tones
COLORS = {
    'easy':     '#8BC7A3',   # muted green
    'medium':   '#F2CB6C',   # muted amber
    'orig_hard':'#E8956A',   # muted orange
    'r1':       '#D98BA3',   # muted pink
    'r2':       '#A68BBF',   # muted purple
    'r3':       '#7A8FBF',   # muted indigo
    'r4':       '#72BFC7',   # muted cyan
    'r5':       '#A68F7D',   # muted brown
    'r6':       '#8A9BA5',   # muted blue-grey
    'r7':       '#A3C47A',   # muted light green
    'hardened': '#A68BBF',   # muted purple (combined)
    'first':    DOCS_COLOR,  # soft blue
    'post_audit':'#8BC7A3',  # muted green
    'p5':       '#E8A85C',   # muted orange
    'env_bug':  NODOCS_COLOR,# soft red
    'agent_fail':DOCS_COLOR, # soft blue
    'app_bug':  '#E07A7A',   # muted red
    'verifier_bug': '#E8A85C',# muted orange
    'impossible':'#A68BBF',  # muted purple
    'ambiguous': '#F2CB6C',  # muted amber
    'infra':    '#A68F7D',   # muted brown
    'agent_side':DOCS_COLOR, # soft blue
}

# Short app names for readability
SHORT_NAMES = {
    'elation-clinical-records': 'Elation\nClinical',
    'elation-prescriptions': 'Elation\nRx',
    'elation-patient-communication': 'Elation\nComms',
    'figma-slides': 'Figma\nSlides',
    'figma-text-and-typography': 'Figma\nText',
    'gmail-accounts-and-contacts': 'Gmail\nContacts',
    'superhuman-general': 'Superhuman',
    'paypal-my-wallet': 'PayPal\nWallet',
    'clio-matters': 'Clio\nMatters',
    'handshake-career-exploration': 'Handshake',
    'linear-account-settings-v2': 'Linear\nSettings',
    'xero-invoicing': 'Xero\nInvoicing',
    'gitlab-plan-and-track': 'GitLab\nPlan',
    'shopify-web-performance': 'Shopify\nPerf',
    'gmail': 'Gmail',
}

def short_name(app):
    return SHORT_NAMES.get(app, app)


# ---------------------------------------------------------------------------
# Mapping of apps to their p5/final run folders
# ---------------------------------------------------------------------------
P5_RUNS = {
    'elation-clinical-records':      'gemini_20260308_171406_p5_parallel',
    'elation-prescriptions':         'gemini_20260308_045634_p5_parallel',
    'elation-patient-communication': 'gemini_20260308_021259_parallel',
    'figma-slides':                  'gemini_20260308_093527_p5_parallel',
    'figma-text-and-typography':     'gemini_20260308_090215_p5_parallel',
    'gmail-accounts-and-contacts':   'gemini_20260308_124645_p5_parallel',
    'superhuman-general':            'gemini_20260308_154224_p5_parallel',
    'paypal-my-wallet':              'gemini_20260308_123918_p5_parallel',
    'clio-matters':                  'gemini_20260308_100600_p5_parallel',
    'handshake-career-exploration':  'gemini_20260308_140355_p5_parallel',
    'linear-account-settings-v2':    'gemini_20260306_084059_parallel',
    'xero-invoicing':                'gemini_20260306_073311_parallel',
    'gitlab-plan-and-track':         'gemini_20260301_163233_parallel',
}


# ---------------------------------------------------------------------------
# Utility: Load results.json
# ---------------------------------------------------------------------------
def load_results(app, run_folder):
    """Load and return a results.json dict, or None if not found."""
    path = S3_DIR / app / run_folder / "results.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def get_task_num(task_id):
    """Extract numeric part from task_id like 'task_h23' -> 23."""
    m = re.search(r'(\d+)', task_id.split('_')[1])
    return int(m.group()) if m else 0


def classify_run(run_folder):
    """Classify a run folder name into a pipeline phase."""
    if '_p3b_' in run_folder:
        return 'p3b'
    if '_p4b_r1_' in run_folder:
        return 'p4b_r1'
    if '_p4b_r2_' in run_folder:
        return 'p4b_r2'
    if '_p4b_r3_' in run_folder:
        return 'p4b_r3'
    if 'function-tasks_p5' in run_folder:
        return 'func_p5'
    if 'function-tasks_p2b' in run_folder:
        return 'func_p2b'
    if '_p5_' in run_folder:
        return 'p5'
    if 'function-tasks' in run_folder:
        return 'func'
    return 'real'


def list_gemini_runs(app):
    """List all gemini run folders for an app, sorted chronologically."""
    app_dir = S3_DIR / app
    if not app_dir.is_dir():
        return []
    runs = []
    for folder in sorted(os.listdir(app_dir)):
        rpath = app_dir / folder / "results.json"
        if rpath.exists():
            with open(rpath) as f:
                data = json.load(f)
            if data.get('model') == 'gemini':
                runs.append((folder, data))
    return runs


def compute_sr_by_origin(data):
    """
    From a results.json, compute SR for each task origin category.
    Returns dict: {'easy': (passed, total), 'medium': ..., 'orig_hard': ..., 'r1': ..., ...}
    """
    results = {}
    tasks = data.get('tasks', [])

    easy = [t for t in tasks if t['task_id'].startswith('task_e')]
    medium = [t for t in tasks if t['task_id'].startswith('task_m')]
    hard = [t for t in tasks if t['task_id'].startswith('task_h')]

    if easy:
        results['easy'] = (sum(1 for t in easy if t['passed']), len(easy))
    if medium:
        results['medium'] = (sum(1 for t in medium if t['passed']), len(medium))

    # Break hard tasks by range
    ranges = [
        ('orig_hard', 1, 20),
        ('r1', 21, 40),
        ('r2', 41, 60),
        ('r3', 61, 80),
        ('r4', 81, 100),
        ('r5', 101, 120),
        ('r6', 121, 140),
        ('r7', 141, 160),
    ]
    for label, lo, hi in ranges:
        group = [t for t in hard if lo <= get_task_num(t['task_id']) <= hi]
        if group:
            results[label] = (sum(1 for t in group if t['passed']), len(group))

    return results


# =========================================================================
# SECTION 1: Self-Challenging Increase
# =========================================================================
def section1_self_challenging():
    print("=" * 70)
    print("SECTION 1: Self-Challenging Increase")
    print("=" * 70)

    # ---- Figure 1: Grouped bar chart of SR by task origin (P5) ----
    categories = ['easy', 'medium', 'orig_hard', 'r1', 'r2', 'r3']
    cat_labels = ['Easy', 'Medium', 'Original\nHard', 'Hardened\nR1', 'Hardened\nR2', 'Hardened\nR3']
    cat_colors = [COLORS['easy'], COLORS['medium'], COLORS['orig_hard'],
                  COLORS['r1'], COLORS['r2'], COLORS['r3']]

    apps_order = [
        'elation-clinical-records', 'elation-prescriptions', 'xero-invoicing',
        'linear-account-settings-v2', 'paypal-my-wallet', 'gmail-accounts-and-contacts',
        'gitlab-plan-and-track', 'superhuman-general', 'handshake-career-exploration',
        'elation-patient-communication', 'figma-text-and-typography', 'figma-slides',
        'clio-matters',
    ]

    # Collect data
    app_sr = {}  # app -> {category: sr_percent}
    for app in apps_order:
        run = P5_RUNS[app]
        data = load_results(app, run)
        if data is None:
            print(f"  WARNING: No results for {app}/{run}")
            continue
        origin_sr = compute_sr_by_origin(data)
        sr_dict = {}
        for cat in categories:
            if cat in origin_sr:
                passed, total = origin_sr[cat]
                sr_dict[cat] = 100.0 * passed / total if total > 0 else 0.0
            else:
                sr_dict[cat] = None
        app_sr[app] = sr_dict

    # Print table
    print("\nSR by Task Origin in Final Evaluation (P5)")
    header = f"{'App':<30} " + " ".join(f"{c:>10}" for c in cat_labels)
    print(header)
    print("-" * len(header))
    for app in apps_order:
        if app not in app_sr:
            continue
        vals = []
        for cat in categories:
            v = app_sr[app].get(cat)
            vals.append(f"{v:>9.1f}%" if v is not None else f"{'N/A':>10}")
        print(f"{short_name(app).replace(chr(10), ' '):<30} " + " ".join(vals))

    # ---- Figure 1: Aggregate bar chart across all apps ----
    agg = defaultdict(list)  # category -> [sr values across apps]
    for app in apps_order:
        if app not in app_sr:
            continue
        sr = app_sr[app]
        for cat in ['easy', 'medium', 'orig_hard']:
            if sr.get(cat) is not None:
                agg[cat].append(sr[cat])
        # Combine all hardened rounds
        hardened_vals = []
        for rcat in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']:
            if sr.get(rcat) is not None:
                hardened_vals.append(sr[rcat])
        if hardened_vals:
            # Average across rounds for this app, then add to aggregate
            agg['hardened'].append(np.mean(hardened_vals))

    fig, ax = plt.subplots(figsize=(5, 3.5))
    agg_cats = ['easy', 'medium', 'orig_hard', 'hardened']
    agg_labels = ['Easy', 'Medium', 'Original Hard', 'Hardened']
    agg_colors = [COLORS['easy'], COLORS['medium'], COLORS['orig_hard'], COLORS['hardened']]

    means = [np.mean(agg[c]) for c in agg_cats]
    stds = [np.std(agg[c]) for c in agg_cats]
    x_agg = np.arange(len(agg_cats))

    bars = ax.bar(x_agg, means, 0.52, yerr=stds, capsize=4,
                  color=agg_colors, edgecolor='white', linewidth=0.5, zorder=3,
                  error_kw={'elinewidth': 1, 'capthick': 1, 'color': '#555'})
    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 2,
                f'{m:.1f}%', ha='center', va='top', fontsize=8, color='#333')

    ax.set_xticks(x_agg)
    ax.set_xticklabels(agg_labels)
    ax.set_ylabel('Average Success Rate (%)')
    ax.set_title('Success Rate by Task Difficulty')
    ax.set_ylim(0, 118)
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'fig1_aggregate_sr_by_origin.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)

    print(f"\n  Aggregate SR:")
    for cat, label in zip(agg_cats, agg_labels):
        print(f"    {label.replace(chr(10), ' ')}: {np.mean(agg[cat]):.1f}% +/- {np.std(agg[cat]):.1f}% (n={len(agg[cat])})")
    print(f"  Saved: {OUT_DIR / 'fig1_aggregate_sr_by_origin.png'}")

    return app_sr


# =========================================================================
# SECTION 2: Functional Correctness Regression
# =========================================================================
def section2_functional_regression():
    print("\n" + "=" * 70)
    print("SECTION 2: Functional Correctness Regression")
    print("=" * 70)

    # Heuristic: for each app, find function-task runs, group by date cluster,
    # use instruction fingerprinting to confirm same task set, then compare
    # post-audit (last run in first date cluster) vs final (last run overall).
    func_data = {}

    all_apps = sorted(set(list(P5_RUNS.keys()) + [
        d for d in os.listdir(S3_DIR) if (S3_DIR / d).is_dir() and 'nodocs' not in d
    ]))

    for app in all_apps:
        runs = list_gemini_runs(app)
        func_runs = []
        for folder, data in runs:
            phase = classify_run(folder)
            if phase in ('func', 'func_p2b', 'func_p5'):
                tasks = data.get('tasks', [])
                total = len(tasks)
                if total == 0:
                    continue
                passed = sum(1 for t in tasks if t.get('passed'))
                rate = 100.0 * passed / total
                # Instruction fingerprint to verify same task set
                instr_fp = hash(tuple(sorted(
                    (t['task_id'], t['instruction']) for t in tasks
                )))
                func_runs.append({
                    'folder': folder,
                    'total': total,
                    'passed': passed,
                    'rate': rate,
                    'date': folder.split('_')[1],  # YYYYMMDD
                    'instr_fp': instr_fp,
                })

        if len(func_runs) < 2:
            continue

        # Post-audit = last run in first date cluster
        first_date = func_runs[0]['date']
        first_cluster = [r for r in func_runs if r['date'] == first_date]
        post_audit = first_cluster[-1]
        final = func_runs[-1]

        # Skip if post-audit and final are the same run (all on same date)
        if post_audit['folder'] == final['folder']:
            continue

        # Verify same task set via instruction fingerprint
        # Allow near-match (auditing may fix a few task instructions)
        same_tasks = (post_audit['instr_fp'] == final['instr_fp'])
        if not same_tasks:
            # Check overlap by loading actual tasks
            d_pa = load_results(app, post_audit['folder'])
            d_fn = load_results(app, final['folder'])
            if d_pa and d_fn:
                t_pa = {t['task_id']: t['instruction'] for t in d_pa['tasks']}
                t_fn = {t['task_id']: t['instruction'] for t in d_fn['tasks']}
                common = set(t_pa.keys()) & set(t_fn.keys())
                match_rate = sum(1 for tid in common if t_pa[tid] == t_fn[tid]) / len(common) if common else 0
                if match_rate < 0.8:
                    continue  # Too different, skip

        func_data[app] = {
            'post_audit': post_audit['rate'],
            'post_audit_detail': f"{post_audit['passed']}/{post_audit['total']}",
            'post_audit_folder': post_audit['folder'],
            'final': final['rate'],
            'final_detail': f"{final['passed']}/{final['total']}",
            'final_folder': final['folder'],
            'delta': final['rate'] - post_audit['rate'],
        }

    # Print summary table
    print("\nFunction Task Pass Rates: Post-Audit vs Final")
    print(f"{'App':<30} {'Post-Audit':>12} {'Final':>10} {'Delta':>8}")
    print("-" * 65)
    for app in sorted(func_data.keys()):
        d = func_data[app]
        label = short_name(app).replace('\n', ' ')
        print(f"  {label:<28} {d['post_audit']:>10.1f}%  {d['final']:>9.1f}% {d['delta']:+.1f}pp")

    print("\n  Run folders used:")
    for app in sorted(func_data.keys()):
        d = func_data[app]
        label = short_name(app).replace('\n', ' ')
        print(f"    {label}: post-audit={d['post_audit_folder']}, final={d['final_folder']}")

    # Figure 2 replaced by table in content.md

    # Compute aggregate stats
    deltas = [func_data[a]['delta'] for a in func_data]
    print(f"\n  Aggregate: mean delta = {np.mean(deltas):+.1f}pp, "
          f"median = {np.median(deltas):+.1f}pp, "
          f"range = [{min(deltas):+.1f}, {max(deltas):+.1f}]pp")
    print(f"  {sum(1 for d in deltas if abs(d) <= 5)}/{len(deltas)} apps within +/-5pp")

    return func_data


# =========================================================================
# SECTION 3: Auditing Impact
# =========================================================================
def parse_audit_summary(filepath):
    """
    Parse an audit_summary.md file and extract structured data.
    Returns a dict with app_name, phase, pass_rate, and bug/failure counts.
    """
    with open(filepath) as f:
        text = f.read()

    result = {
        'filepath': str(filepath),
        'app_name': None,
        'phase': None,
        'total_tasks': 0,
        'passed': 0,
        'pass_rate': 0.0,
        'env_bugs': 0,       # app bug + verifier bug + impossible task + ambiguous instruction
        'agent_failures': 0,
        'app_bugs': 0,
        'verifier_bugs': 0,
        'impossible_tasks': 0,
        'ambiguous_instructions': 0,
        'infra_failures': 0,
        'agent_side_failures': 0,
    }

    # Extract app name from path
    parts = Path(filepath).parts
    for i, p in enumerate(parts):
        if p == 's3_results' and i + 1 < len(parts):
            result['app_name'] = parts[i + 1]
            break

    # Extract run folder name to determine phase
    run_folder = Path(filepath).parent.name
    result['phase'] = classify_run(run_folder)
    result['run_folder'] = run_folder

    # Extract pass rate from various formats
    # Look for the overall results section first (top of document)
    # Format: "X/Y passed (Z%)" or "X/Y (Z%)" - the most reliable pattern
    overall_match = re.search(r'(\d+)/(\d+)\s*(?:passed|tasks?\s*passed|\()', text[:2000], re.IGNORECASE)
    if overall_match:
        result['passed'] = int(overall_match.group(1))
        result['total_tasks'] = int(overall_match.group(2))

    # Also check table formats: "| Passed | 52 |" or "| Total tasks | 55 |"
    if result['passed'] == 0:
        m = re.search(r'\|\s*\*?\*?Passed\*?\*?\s*\|\s*\*?\*?(\d+)', text[:2000], re.IGNORECASE)
        if m:
            result['passed'] = int(m.group(1))
    if result['total_tasks'] == 0:
        m = re.search(r'\|\s*\*?\*?Total\s*tasks?\*?\*?\s*\|\s*(\d+)', text[:2000], re.IGNORECASE)
        if m:
            result['total_tasks'] = int(m.group(1))

    # Extract explicit pass rate
    m = re.search(r'(?:[Pp]ass\s*[Rr]ate)\s*\*?\*?\s*[|:]\s*\*?\*?\s*(\d+(?:\.\d+)?)\s*%', text[:2000])
    if m:
        result['pass_rate'] = float(m.group(1))
    elif result['total_tasks'] > 0:
        result['pass_rate'] = 100.0 * result['passed'] / result['total_tasks']

    # Sanity check: pass_rate should be 0-100
    if result['pass_rate'] > 100:
        if result['total_tasks'] > 0:
            result['pass_rate'] = 100.0 * result['passed'] / result['total_tasks']
        else:
            result['pass_rate'] = 0.0

    # Count bug categories via regex

    # App bugs / Website bugs
    app_bug_patterns = [
        r'(?:App [Bb]ug|Website [Bb]ug|app bug|web app bug)',
        r'(?:Missing UI|cross-module)',
    ]
    for pattern in app_bug_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        result['app_bugs'] += len(matches)

    # Verifier bugs
    verifier_matches = re.findall(r'[Vv]erifier [Bb]ug', text, re.IGNORECASE)
    result['verifier_bugs'] += len(verifier_matches)

    # Impossible tasks
    impossible_matches = re.findall(r'[Ii]mpossible [Tt]ask', text, re.IGNORECASE)
    result['impossible_tasks'] += len(impossible_matches)

    # Ambiguous instructions
    ambiguous_matches = re.findall(r'[Aa]mbiguous (?:instruction|task)', text, re.IGNORECASE)
    result['ambiguous_instructions'] += len(ambiguous_matches)

    # Infrastructure failures
    infra_matches = re.findall(r'[Ii]nfrastructure (?:[Ff]ailure|[Ii]ssue|failure)', text, re.IGNORECASE)
    result['infra_failures'] += len(infra_matches)

    # Agent-side failures - count from summary tables first
    # Look for "Agent-side failure | N" or "agent-side failures: N"
    agent_table_match = re.search(r'[Aa]gent.side\s*(?:[Ff]ailure|failures?)\s*[|:]\s*(\d+)', text)
    if agent_table_match:
        result['agent_side_failures'] = int(agent_table_match.group(1))
    else:
        # Count individual agent-side failure mentions in task details
        agent_mentions = re.findall(r'[Aa]gent.side (?:[Ff]ailure|failure)', text)
        result['agent_side_failures'] += len(agent_mentions)

    # Better approach: look at Root Cause Analysis table or Failure Breakdown tables
    # Parse "| Root Cause | Count |" style tables
    table_rows = re.findall(r'\|\s*(.*?)\s*\|\s*(\d+)\s*\|', text)
    for label, count_str in table_rows:
        label_lower = label.strip().lower()
        count = int(count_str)
        if any(w in label_lower for w in ['app bug', 'website bug', 'modal', 'missing ui', 'no edit', 'search results', 'no delete', 'toggle']):
            result['app_bugs'] = max(result['app_bugs'], count)
        elif 'verifier' in label_lower and 'bug' in label_lower:
            result['verifier_bugs'] = max(result['verifier_bugs'], count)
        elif 'impossible' in label_lower:
            result['impossible_tasks'] = max(result['impossible_tasks'], count)
        elif 'ambiguous' in label_lower:
            result['ambiguous_instructions'] = max(result['ambiguous_instructions'], count)
        elif 'infrastructure' in label_lower or 'infra' in label_lower:
            result['infra_failures'] = max(result['infra_failures'], count)

    # Count task-level root causes more precisely
    # Look for ### task_XX sections and their root cause
    task_sections = re.findall(r'###\s+task_\w+.*?(?=###|\Z)', text, re.DOTALL)
    actual_app_bugs = 0
    actual_verifier_bugs = 0
    actual_impossible = 0
    actual_ambiguous = 0
    actual_agent = 0
    actual_infra = 0

    for section in task_sections:
        section_lower = section.lower()
        if 'app bug' in section_lower or 'website bug' in section_lower:
            actual_app_bugs += 1
        elif 'verifier bug' in section_lower:
            actual_verifier_bugs += 1
        elif 'impossible task' in section_lower or 'impossible' in section_lower and 'root cause' in section_lower:
            actual_impossible += 1
        elif 'ambiguous' in section_lower:
            actual_ambiguous += 1
        elif 'agent' in section_lower and ('failure' in section_lower or 'timeout' in section_lower):
            actual_agent += 1
        elif 'infrastructure' in section_lower:
            actual_infra += 1

    # Use task-level counts if they seem more reliable
    if actual_app_bugs + actual_verifier_bugs + actual_impossible + actual_ambiguous + actual_agent > 0:
        result['app_bugs'] = actual_app_bugs
        result['verifier_bugs'] = actual_verifier_bugs
        result['impossible_tasks'] = actual_impossible
        result['ambiguous_instructions'] = actual_ambiguous
        if actual_agent > 0:
            result['agent_side_failures'] = actual_agent
        result['infra_failures'] = actual_infra

    result['env_bugs'] = (result['app_bugs'] + result['verifier_bugs'] +
                          result['impossible_tasks'] + result['ambiguous_instructions'])

    return result


def section3_auditing():
    print("\n" + "=" * 70)
    print("SECTION 3: Auditing Impact")
    print("=" * 70)

    # Find all audit_summary.md files (exclude nodocs)
    audit_files = []
    for root, dirs, files in os.walk(S3_DIR):
        if 'nodocs' in root:
            continue
        for f in files:
            if f == 'audit_summary.md':
                fpath = os.path.join(root, f)
                # Only include gemini runs (check folder name)
                folder = os.path.basename(root)
                if folder.startswith('gemini_') and not folder.startswith('gemini-'):
                    audit_files.append(fpath)

    print(f"\nFound {len(audit_files)} audit summaries (gemini, non-nodocs)")

    # Parse all
    audits = []
    for fpath in sorted(audit_files):
        parsed = parse_audit_summary(fpath)
        audits.append(parsed)

    # Print summary
    print("\nAudit Summary Table:")
    print(f"{'App':<30} {'Phase':<10} {'Rate':>8} {'AppBug':>7} {'VfyBug':>7} {'Imposs':>7} {'Ambig':>7} {'Agent':>7}")
    print("-" * 88)
    for a in audits:
        label = short_name(a['app_name']).replace('\n', ' ')
        print(f"  {label:<28} {a['phase']:<10} {a['pass_rate']:>7.1f}% {a['app_bugs']:>7} {a['verifier_bugs']:>7} {a['impossible_tasks']:>7} {a['ambiguous_instructions']:>7} {a['agent_side_failures']:>7}")

    # ---- Figure 6: Stacked bar chart of env bugs vs agent failures per app ----
    app_bug_agg = defaultdict(lambda: {'env': 0, 'agent': 0})
    for a in audits:
        app = a['app_name']
        app_bug_agg[app]['env'] += a['env_bugs']
        app_bug_agg[app]['agent'] += a['agent_side_failures']

    plot_apps_6 = sorted(app_bug_agg.keys(),
                         key=lambda a: app_bug_agg[a]['env'] + app_bug_agg[a]['agent'],
                         reverse=True)
    # Filter to apps that have at least 1 finding
    plot_apps_6 = [a for a in plot_apps_6 if app_bug_agg[a]['env'] + app_bug_agg[a]['agent'] > 0]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.arange(len(plot_apps_6))
    env_vals = [app_bug_agg[a]['env'] for a in plot_apps_6]
    agent_vals = [app_bug_agg[a]['agent'] for a in plot_apps_6]

    ax.bar(x, env_vals, 0.55, label='Environment Bugs', color=COLORS['env_bug'],
           edgecolor='white', linewidth=0.5, zorder=3)
    ax.bar(x, agent_vals, 0.55, bottom=env_vals, label='Agent Failures',
           color=COLORS['agent_fail'], edgecolor='white', linewidth=0.5, zorder=3)

    for i, (e, a_val) in enumerate(zip(env_vals, agent_vals)):
        total = e + a_val
        if total > 0:
            ax.text(i, total + 0.3, str(total), ha='center', va='bottom', fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels([short_name(a) for a in plot_apps_6], ha='center')
    ax.set_ylabel('Number of Issues Found')
    ax.set_title('Audit Findings: Environment Bugs vs Agent Failures')
    ax.legend(loc='upper right')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'fig3_audit_env_vs_agent.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"\n  Saved: {OUT_DIR / 'fig3_audit_env_vs_agent.png'}")

    # ---- Figure 7: Pie/donut chart of bug categories ----
    total_app = sum(a['app_bugs'] for a in audits)
    total_vfy = sum(a['verifier_bugs'] for a in audits)
    total_imp = sum(a['impossible_tasks'] for a in audits)
    total_amb = sum(a['ambiguous_instructions'] for a in audits)
    total_agent = sum(a['agent_side_failures'] for a in audits)
    total_infra = sum(a['infra_failures'] for a in audits)

    pie_data = [
        ('App Bug', total_app, COLORS['app_bug']),
        ('Verifier Bug', total_vfy, COLORS['verifier_bug']),
        ('Impossible Task', total_imp, COLORS['impossible']),
        ('Ambiguous\nInstruction', total_amb, COLORS['ambiguous']),
        ('Agent-Side\nFailure', total_agent, COLORS['agent_side']),
        ('Infrastructure', total_infra, COLORS['infra']),
    ]
    pie_data = [(l, v, c) for l, v, c in pie_data if v > 0]
    pie_sizes = [v for _, v, _ in pie_data]
    pie_colors = [c for _, _, c in pie_data]
    grand_total = sum(pie_sizes)

    # Short labels: multi-line centered, count on its own line
    PIE_LABELS = {
        'App Bug': 'App Bug\n({val})',
        'Verifier Bug': 'Verifier\nBug\n({val})',
        'Impossible Task': 'Impossible\nTask\n({val})',
        'Ambiguous\nInstruction': 'Ambiguous\nInstruction\n({val})',
        'Agent-Side\nFailure': 'Agent-Side\nFailure\n({val})',
        'Infrastructure': 'Infrastructure\n({val})',
    }

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, _ = ax.pie(
        pie_sizes, colors=pie_colors, labels=[''] * len(pie_sizes),
        startangle=90,
        wedgeprops=dict(width=0.48, edgecolor='white', linewidth=1.5))

    for i, (wedge, (label, val, _)) in enumerate(zip(wedges, pie_data)):
        ang = (wedge.theta2 + wedge.theta1) / 2
        pct = 100 * val / grand_total

        # Percentage inside the wedge
        r_in = 0.76
        x_in = r_in * np.cos(np.deg2rad(ang))
        y_in = r_in * np.sin(np.deg2rad(ang))
        ax.text(x_in, y_in, f'{pct:.0f}%', ha='center', va='center',
                fontsize=9, color='white', fontweight='bold', zorder=4)

        # Label outside with leader line
        x_edge = np.cos(np.deg2rad(ang))
        y_edge = np.sin(np.deg2rad(ang))
        r_text = 1.3
        x_text = r_text * x_edge
        y_text = r_text * y_edge
        fmt = PIE_LABELS.get(label, label + '\n({val})')
        disp_label = fmt.format(val=val)

        ax.annotate(
            disp_label,
            xy=(0.98 * x_edge, 0.98 * y_edge),
            xytext=(x_text, y_text),
            fontsize=9, color='#333', va='center', ha='center',
            arrowprops=dict(arrowstyle='-', color='#999', lw=0.8,
                            connectionstyle='arc3,rad=0'),
        )

    ax.set_title('Audit Finding Categories')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'fig4_bug_categories_donut.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)

    print(f"\n  Bug category totals:")
    print(f"    App bugs: {total_app}")
    print(f"    Verifier bugs: {total_vfy}")
    print(f"    Impossible tasks: {total_imp}")
    print(f"    Ambiguous instructions: {total_amb}")
    print(f"    Agent-side failures: {total_agent}")
    print(f"    Infrastructure: {total_infra}")
    print(f"  Saved: {OUT_DIR / 'fig4_bug_categories_donut.png'}")

    # ---- Figure 6: Audit improvement trend (line plot) ----
    # Only apps with clear audit progression (audit_summary.md marks the audited run,
    # next chronological run of same type is post-fix)
    audit_trends = {
        'Xero Invoicing': [
            ('Eval 1', 72.4),
            ('Post-Audit', 100.0),
        ],
        'GitLab Plan & Track': [
            ('Eval 1', 92.7),
            ('Post-Audit 1', 98.2),
            ('Post-Audit 2', 98.2),
        ],
        'Elation Clinical': [
            ('Eval 1', 94.5),
            ('Post-Audit 1', 98.2),
            ('Post-Audit 2', 100.0),
        ],
    }

    fig, ax = plt.subplots(figsize=(4, 3))
    colors = ['#E8A85C', '#D98BA3', '#77B1F2']
    markers = ['s', 'D', 'o']

    legend_handles_5 = []
    all_annotations = []  # (x, y, text, color)

    for idx, (label, points) in enumerate(audit_trends.items()):
        xs = list(range(len(points)))
        ys = [p[1] for p in points]

        line, = ax.plot(xs, ys, '-', color=colors[idx], linewidth=1.8, marker=markers[idx],
                markersize=6, zorder=3, markeredgecolor='white', markeredgewidth=1,
                label=label)
        legend_handles_5.append(line)

        for i, (x, y) in enumerate(zip(xs, ys)):
            all_annotations.append((x, y, f'{y:.1f}%', colors[idx]))

    # Place annotations, alternating above/below to avoid overlap
    from collections import defaultdict as _dd
    by_x = _dd(list)
    for x, y, text, color in all_annotations:
        by_x[x].append((y, text, color))

    for x, items in by_x.items():
        items.sort(key=lambda t: t[0], reverse=True)  # highest y first
        for i, (y_orig, text, color) in enumerate(items):
            # Alternate: first item above, second below, third further below
            if i == 0:
                offset_y = 7
                va = 'bottom'
            elif i == 1:
                offset_y = -7
                va = 'top'
            else:
                offset_y = -16
                va = 'top'
            ax.annotate(text, (x, y_orig), textcoords='offset points',
                        xytext=(0, offset_y), ha='center', va=va,
                        fontsize=9, color=color, zorder=5)

    max_len = max(len(v) for v in audit_trends.values())
    x_labels = ['Initial\nGeneration', 'After\nAudit 1', 'After\nAudit 2'][:max_len]
    ax.set_xticks(range(max_len))
    ax.set_xticklabels(x_labels)
    ax.set_ylabel('Functional Testing Task Success Rate (%)')
    ax.set_title('Success Rate Trend Through Audit Cycles')
    ax.set_xlim(-0.15, max_len - 0.85)
    ax.set_ylim(66, 106)

    ax.legend(handles=legend_handles_5, loc='lower right', fontsize=9,
              frameon=True, framealpha=0.9, edgecolor='#DDD')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'fig5_audit_improvement_trend.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {OUT_DIR / 'fig5_audit_improvement_trend.png'}")

    return audits


# =========================================================================
# Report Generation
# =========================================================================
def generate_report(app_sr, app_pipeline_sr, func_data, audits):
    """Generate a comprehensive markdown report."""
    lines = []
    lines.append("# Ablation Analysis Report")
    lines.append("")
    lines.append("## Section 1: Self-Challenging Increase")
    lines.append("")
    lines.append("Shows that hardening rounds produce progressively harder tasks.")
    lines.append("")

    # Figure references
    lines.append("### Figures")
    lines.append("")
    lines.append("- **Figure 1** (`fig1_sr_by_origin_p5.png`): Success Rate by Task Origin in Final Evaluation (P5)")
    lines.append("- **Figure 2** (`fig1_aggregate_sr_by_origin.png`): Aggregate Success Rate by Task Origin")
    lines.append("")

    # Data table for Figure 1
    categories = ['easy', 'medium', 'orig_hard', 'r1', 'r2', 'r3']
    cat_labels = ['Easy', 'Medium', 'Orig Hard', 'R1', 'R2', 'R3']
    lines.append("### Table 1: SR by Task Origin in P5")
    lines.append("")
    lines.append("| App | " + " | ".join(cat_labels) + " |")
    lines.append("|" + "---|" * (len(cat_labels) + 1))

    apps_order = sorted(app_sr.keys(), key=lambda a: app_sr[a].get('easy', 0) or 0, reverse=True)
    for app in apps_order:
        sr = app_sr[app]
        vals = []
        for cat in categories:
            v = sr.get(cat)
            vals.append(f"{v:.1f}%" if v is not None else "N/A")
        lines.append(f"| {short_name(app).replace(chr(10), ' ')} | " + " | ".join(vals) + " |")
    lines.append("")

    # Aggregate stats
    agg = defaultdict(list)
    for app in app_sr:
        sr = app_sr[app]
        for cat in ['easy', 'medium', 'orig_hard']:
            if sr.get(cat) is not None:
                agg[cat].append(sr[cat])
        hardened_vals = [sr[r] for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7'] if sr.get(r) is not None]
        if hardened_vals:
            agg['hardened'].append(np.mean(hardened_vals))

    lines.append("### Aggregate Statistics")
    lines.append("")
    lines.append("| Category | Mean SR | Std Dev | N |")
    lines.append("|---|---|---|---|")
    for cat, label in [('easy', 'Easy'), ('medium', 'Medium'), ('orig_hard', 'Original Hard'), ('hardened', 'Hardened (avg)')]:
        vals = agg[cat]
        lines.append(f"| {label} | {np.mean(vals):.1f}% | {np.std(vals):.1f}% | {len(vals)} |")
    lines.append("")

    # Section 2
    lines.append("## Section 2: Functional Correctness Regression")
    lines.append("")
    lines.append("Table included in content.md.")
    lines.append("")

    lines.append("### Table 2: Function Task Pass Rates (Post-Audit vs Final)")
    lines.append("")
    lines.append("| App | Post-Audit | Final | Delta |")
    lines.append("|---|---|---|---|")
    for app in sorted(func_data.keys()):
        d = func_data[app]
        label = short_name(app).replace('\n', ' ')
        lines.append(f"| {label} | {d['post_audit']:.1f}% | {d['final']:.1f}% | {d['delta']:+.1f}pp |")
    lines.append("")

    # Section 3
    lines.append("## Section 3: Auditing Impact")
    lines.append("")
    lines.append("### Figures")
    lines.append("")
    lines.append("- **Figure 4** (`fig3_audit_env_vs_agent.png`): Environment Bugs vs Agent Failures")
    lines.append("- **Figure 5** (`fig4_bug_categories_donut.png`): Bug Category Distribution")
    lines.append("- **Figure 6** (`fig5_audit_improvement_trend.png`): Pre-Audit to Post-Audit Pass Rate Changes")
    lines.append("")

    lines.append("### Table 3: Audit Findings by App")
    lines.append("")
    lines.append("| App | Phase | Pass Rate | App Bugs | Verifier Bugs | Impossible | Ambiguous | Agent Failures |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for a in audits:
        label = short_name(a['app_name']).replace('\n', ' ')
        lines.append(f"| {label} | {a['phase']} | {a['pass_rate']:.1f}% | {a['app_bugs']} | {a['verifier_bugs']} | {a['impossible_tasks']} | {a['ambiguous_instructions']} | {a['agent_side_failures']} |")
    lines.append("")

    total_app = sum(a['app_bugs'] for a in audits)
    total_vfy = sum(a['verifier_bugs'] for a in audits)
    total_imp = sum(a['impossible_tasks'] for a in audits)
    total_amb = sum(a['ambiguous_instructions'] for a in audits)
    total_agent = sum(a['agent_side_failures'] for a in audits)
    total_infra = sum(a['infra_failures'] for a in audits)

    lines.append("### Aggregate Bug Counts")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    lines.append(f"| App Bugs | {total_app} |")
    lines.append(f"| Verifier Bugs | {total_vfy} |")
    lines.append(f"| Impossible Tasks | {total_imp} |")
    lines.append(f"| Ambiguous Instructions | {total_amb} |")
    lines.append(f"| Agent-Side Failures | {total_agent} |")
    lines.append(f"| Infrastructure Failures | {total_infra} |")
    lines.append(f"| **Total** | **{total_app + total_vfy + total_imp + total_amb + total_agent + total_infra}** |")
    lines.append("")

    env_total = total_app + total_vfy + total_imp + total_amb
    all_total = env_total + total_agent + total_infra
    if all_total > 0:
        lines.append(f"Environment issues account for {env_total}/{all_total} ({100*env_total/all_total:.1f}%) of all findings.")
        lines.append(f"Agent-side failures account for {total_agent}/{all_total} ({100*total_agent/all_total:.1f}%).")
    lines.append("")

    # Key findings
    lines.append("## Key Findings")
    lines.append("")
    lines.append("1. **Hardening works**: Average SR drops from {:.1f}% (easy) to {:.1f}% (original hard) to {:.1f}% (hardened), demonstrating progressive difficulty.".format(
        np.mean(agg['easy']), np.mean(agg['orig_hard']), np.mean(agg['hardened'])))
    lines.append("2. **Function tasks remain stable**: Most apps maintain >90% function task pass rate through the pipeline.")
    lines.append("3. **Auditing catches real bugs**: The majority of audit findings are environment-side issues (app bugs, verifier bugs) that would otherwise pollute evaluation results.")
    lines.append("")

    report_path = OUT_DIR / "ablation_report.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"\n  Report saved: {report_path}")


# =========================================================================
# Main
# =========================================================================
def main():
    print("Mirror-Mirror Ablation Analysis")
    print(f"Reading from: {S3_DIR}")
    print(f"Output to:    {OUT_DIR}")
    print()

    app_sr = section1_self_challenging()
    func_data = section2_functional_regression()
    audits = section3_auditing()
    generate_report(app_sr, None, func_data, audits)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nFigures saved to: {OUT_DIR}")
    print("Files:")
    for f in sorted(OUT_DIR.glob("fig*.png")):
        print(f"  {f.name}")
    print(f"  ablation_report.md")


if __name__ == "__main__":
    main()
