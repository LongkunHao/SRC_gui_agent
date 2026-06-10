#!/usr/bin/env python3
"""
Feature extraction for docs-vs-nodocs authenticity analysis.

- Docs: Gemini Flash (batched over doc files)
- Apps: Claude CLI (reads JS code + tasks + description)

Outputs cached JSON per app pair to analysis/cache/features/.
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/ubuntu/mirror-mirror")
CACHE_DIR = REPO / "analysis" / "cache" / "features"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MAX_HARD_ID = 60

# ── Gemini client ──────────────────────────────────────────────────────────

_gemini_client = None

def get_gemini():
    global _gemini_client
    if _gemini_client is None:
        from google import genai
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


def gemini_extract(prompt: str, max_retries: int = 3) -> list[str]:
    """Call Gemini Flash to extract features."""
    client = get_gemini()
    for attempt in range(max_retries):
        try:
            resp = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            lines = [l.strip().lstrip("0123456789.-*) ") for l in resp.text.strip().split("\n")]
            return [l for l in lines if len(l) > 3]
        except Exception as e:
            wait = min(2 ** (attempt + 2), 65)
            print(f"      Gemini retry {attempt+1}, waiting {wait}s: {e}")
            time.sleep(wait)
    return []


# ── Claude CLI ─────────────────────────────────────────────────────────────

def claude_extract(code: str, prompt: str, timeout: int = 120) -> list[str]:
    """Call Claude CLI to extract features from code."""
    full_input = code
    cmd = ["claude", "--print", prompt]
    try:
        result = subprocess.run(
            cmd, input=full_input, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            print(f"      Claude CLI error: {result.stderr[:200]}")
            return []
        lines = [l.strip().lstrip("0123456789.-*) ") for l in result.stdout.strip().split("\n")]
        return [l for l in lines if len(l) > 3]
    except subprocess.TimeoutExpired:
        print("      Claude CLI timed out")
        return []


# ── Extraction prompts ─────────────────────────────────────────────────────

PROMPT_DOCS = """Extract all distinct user-facing features and capabilities described in this product documentation.
Each feature should be a short phrase describing something a user can DO (an action or capability).
Output one feature per line, no numbering, no bullets.
Be specific but abstract away from specific entity names.
Only include features that are clearly described, not implied.

Document:
{text}"""

PROMPT_CODE = """You are analyzing a web application's JavaScript source code. Extract all distinct user-facing functional capabilities that this application implements.

Each capability should be a short phrase describing something a user can DO (an action or capability).
- Be specific: 'approve an invoice' not 'perform an action'
- Abstract away from specific entity names: 'create a contact' not 'create Murray River Winery contact'
- Include both direct actions (create, delete) and configuration/settings capabilities
- Include navigation capabilities (views, pages the user can access)
- Do NOT include internal implementation details (event listeners, DOM manipulation, state management)

Output one capability per line, no numbering, no bullets, no explanation."""

PROMPT_TASKS = """Below are task instructions for a web application. Extract the distinct functional capabilities that the application must support to enable these tasks.
Each capability should be a short phrase describing something a user can DO.
Deduplicate: if multiple tasks test the same capability, list it once.
Abstract away from specific entity names (e.g. "approve an invoice" not "approve the Murray River Winery invoice").
Output one capability per line, no numbering, no bullets.

Tasks:
{text}"""

PROMPT_APP_DESC = """Extract all distinct user-facing features and capabilities from this web application description.
Each feature should be a short phrase describing something a user can DO.
Output one feature per line, no numbering, no bullets.

Application Description:
{text}"""


# ── Main extraction functions ──────────────────────────────────────────────

def extract_doc_features(docs_path: Path) -> list[str]:
    """Extract features from product documentation using Gemini."""
    all_features = set()

    if docs_path.is_file():
        # Entry point — resolve links
        base_dir = docs_path.parent
        entry_text = docs_path.read_text(errors="replace")
        import re
        links = re.findall(r'\(([^)]+\.md)\)', entry_text)
        md_files = [docs_path]
        for link in links:
            target = (base_dir / link).resolve()
            if target.is_file():
                md_files.append(target)
    elif docs_path.is_dir():
        md_files = sorted(docs_path.rglob("*.md"))
    else:
        return []

    print(f"    Processing {len(md_files)} doc files with Gemini...")

    # Batch files into ~25K char chunks
    batch_text = ""
    batch_count = 0
    for mf in md_files:
        content = mf.read_text(errors="replace")
        batch_text += f"\n\n---\n\n{content}"
        batch_count += 1
        if len(batch_text) > 25000 or mf == md_files[-1]:
            features = gemini_extract(PROMPT_DOCS.format(text=batch_text))
            all_features.update(features)
            print(f"      Batch ({batch_count} files) -> {len(features)} features")
            batch_text = ""
            batch_count = 0

    return sorted(all_features)


def extract_app_code_features(app_dir: Path) -> list[str]:
    """Extract features from app code only via Claude CLI."""
    js_dir = app_dir / "js"
    if not js_dir.exists():
        return []

    js_files = sorted(js_dir.glob("*.js"))
    code = ""
    for f in js_files:
        code += f"\n// === {f.name} ===\n" + f.read_text(errors="replace")

    print(f"    Extracting from code ({len(code)} chars) via Claude...")
    features = claude_extract(code, PROMPT_CODE)
    print(f"      Code -> {len(features)} features")
    return sorted(set(features))


def extract_app_features(app_dir: Path, code_features: list[str] | None = None) -> list[str]:
    """Extract features from an app using Claude (code) and Gemini (tasks/desc)."""
    all_features = set()

    # 1. Code features (reuse if already extracted)
    if code_features is not None:
        all_features.update(code_features)
    else:
        all_features.update(extract_app_code_features(app_dir))

    # 2. Task instructions via Gemini
    tasks_path = app_dir / "real-tasks.json"
    if tasks_path.exists():
        with open(tasks_path) as f:
            tasks = json.load(f)
        tasks = [t for t in tasks
                 if not (t["id"].startswith("task_h") and int(t["id"].split("_h")[1]) > MAX_HARD_ID)]
        task_text = "\n".join(f"- {t['instruction']}" for t in tasks)
        features = gemini_extract(PROMPT_TASKS.format(text=task_text))
        all_features.update(features)
        print(f"      Tasks ({len(tasks)}) -> {len(features)} features")

    # 3. APP_DESCRIPTION.md via Gemini
    desc_path = app_dir / "APP_DESCRIPTION.md"
    if desc_path.exists():
        desc = desc_path.read_text(errors="replace")
        features = gemini_extract(PROMPT_APP_DESC.format(text=desc[:30000]))
        all_features.update(features)
        print(f"      APP_DESCRIPTION -> {len(features)} features")

    return sorted(all_features)


# ── Cache management ───────────────────────────────────────────────────────

def cache_path(name: str, variant: str) -> Path:
    return CACHE_DIR / f"{name}_{variant}.json"


def load_cached(name: str, variant: str) -> list[str] | None:
    p = cache_path(name, variant)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return None


def save_cached(name: str, variant: str, features: list[str]):
    with open(cache_path(name, variant), "w") as f:
        json.dump(features, f, indent=2)


# ── Main ───────────────────────────────────────────────────────────────────

PAIRS = [
    ("elation-prescriptions", "apps/user-manuals/elation/prescriptions"),
    ("figma-slides", "apps/user-manuals/figma/figma-slides"),
    ("gitlab-plan-and-track", "apps/user-manuals/gitlab/topics/plan_and_track.md"),
    ("gmail-accounts-and-contacts", "apps/user-manuals/gmail/accounts-and-contacts"),
    ("xero-invoicing", "apps/user-manuals/xero/invoicing"),
]


def main():
    force = "--force" in sys.argv

    for name, docs_rel in PAIRS:
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")

        docs_path = REPO / docs_rel
        docs_app = REPO / "apps" / name
        nodocs_app = REPO / "apps" / "ablations" / f"{name}-nodocs"

        # Doc features
        cached = load_cached(name, "docs")
        if cached and not force:
            print(f"  Docs: cached ({len(cached)} features)")
            doc_features = cached
        else:
            print(f"  Docs: extracting...")
            doc_features = extract_doc_features(docs_path)
            save_cached(name, "docs", doc_features)
            print(f"  Docs: {len(doc_features)} features")

        # With-docs app: code-only features + merged features
        for app_label, app_path in [("docs_app", docs_app), ("nodocs_app", nodocs_app)]:
            # Code-only extraction
            code_cached = load_cached(name, f"{app_label}_code")
            if code_cached and not force:
                print(f"  {app_label} code: cached ({len(code_cached)} features)")
                code_features = code_cached
            else:
                print(f"  {app_label} code: extracting...")
                code_features = extract_app_code_features(app_path)
                save_cached(name, f"{app_label}_code", code_features)
                print(f"  {app_label} code: {len(code_features)} features")

            # Merged (code + tasks + desc)
            merged_cached = load_cached(name, app_label)
            if merged_cached and not force:
                print(f"  {app_label} merged: cached ({len(merged_cached)} features)")
            else:
                print(f"  {app_label} merged: extracting...")
                features = extract_app_features(app_path, code_features=code_features)
                save_cached(name, app_label, features)
                print(f"  {app_label} merged: {len(features)} features")

    print(f"\n{'='*60}")
    print(f"Done. Features cached in {CACHE_DIR}")


if __name__ == "__main__":
    main()
