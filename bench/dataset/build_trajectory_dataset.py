#!/usr/bin/env python3
"""
Build and upload the WebArena-Infinity trajectory dataset to HuggingFace.

Two-phase pipeline:
  Phase 1 (--download):  Generate manifest + download raw task data from S3
  Phase 2 (--upload):    Upload raw data + README to HuggingFace Hub

Usage:
  # Download successful trajectories from S3
  python build_trajectory_dataset.py --download --workers 32

  # Upload to HuggingFace (creates/updates a private dataset repo)
  python build_trajectory_dataset.py --upload

  # Both in one go
  python build_trajectory_dataset.py --download --upload --workers 32
"""

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
BENCH_DIR = SCRIPT_DIR.parent
REPO_ROOT = BENCH_DIR.parent

S3_BUCKET = os.environ.get("MM_S3_BUCKET", "mirror-mirror-results")

# Where raw task data lands after download
RAW_DIR = SCRIPT_DIR / "raw"

# All 13 environments
ALL_ENVS = [
    "elation-clinical-records",
    "elation-patient-communication",
    "elation-prescriptions",
    "figma-slides",
    "figma-text-and-typography",
    "gitlab-plan-and-track",
    "gmail",
    "gmail-accounts-and-contacts",
    "handshake-career-exploration",
    "linear-account-settings",
    "paypal-my-wallet",
    "superhuman-general",
    "xero-invoicing",
]

MODELS = ["gemini", "kimi", "qwen"]

# Gemini uses a different folder name for linear
GEMINI_ENV_MAP = {e: e for e in ALL_ENVS}
GEMINI_ENV_MAP["linear-account-settings"] = "linear-account-settings-v2"


# ---------------------------------------------------------------------------
# Phase 1: Download
# ---------------------------------------------------------------------------

def find_final_run(s3_results_dir: Path, env_folder: str) -> tuple[str | None, dict | None]:
    """Find the latest valid run for an env from local s3_results cache."""
    env_dir = s3_results_dir / env_folder
    if not env_dir.exists():
        return None, None

    run_dirs = sorted(env_dir.iterdir(), reverse=True)
    for run_dir in run_dirs:
        if not run_dir.is_dir():
            continue
        for rj_path in [run_dir / "merged" / "results.json", run_dir / "results.json"]:
            if rj_path.exists() and rj_path.stat().st_size > 100:
                try:
                    data = json.loads(rj_path.read_text())
                    if data.get("total", 0) > 0:
                        return run_dir.name, data
                except (json.JSONDecodeError, KeyError):
                    continue
    return None, None


def build_manifest() -> list[dict]:
    """Build a manifest of all successful tasks to download."""
    manifest = []

    for model in MODELS:
        s3_results_dir = BENCH_DIR / f"s3_results_{model}"
        if not s3_results_dir.exists():
            print(f"  WARNING: {s3_results_dir} not found, skipping {model}")
            continue

        for env in ALL_ENVS:
            env_folder = GEMINI_ENV_MAP[env] if model == "gemini" else env
            run_name, data = find_final_run(s3_results_dir, env_folder)

            if not data:
                print(f"  WARNING: no valid run for {model}/{env}")
                continue

            for task in data.get("tasks", []):
                if not task.get("passed", False):
                    continue

                source_run = task.get("source_run", "run1")
                task_id = task["task_id"]

                manifest.append({
                    "model": model,
                    "environment": env,
                    "task_id": task_id,
                    "difficulty": task.get("difficulty", ""),
                    "instruction": task.get("instruction", ""),
                    "elapsed": task.get("elapsed", 0),
                    "steps": task.get("steps", 0),
                    "verifier_message": task.get("verifier_message", ""),
                    # S3 path components
                    "s3_env": env_folder,
                    "run_name": run_name,
                    "source_run": source_run,
                })

    return manifest


def download_task(entry: dict) -> str | None:
    """Download screenshots + history.json + result.json for one task from S3."""
    model = entry["model"]
    env = entry["environment"]
    task_id = entry["task_id"]
    s3_env = entry["s3_env"]
    run_name = entry["run_name"]
    source_run = entry["source_run"]

    s3_prefix = f"s3://{S3_BUCKET}/{s3_env}/{run_name}/{source_run}/{task_id}/"
    local_dir = RAW_DIR / model / env / task_id

    if _task_already_downloaded(local_dir):
        return None  # already done

    local_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [
                "aws", "s3", "sync", s3_prefix, str(local_dir) + "/",
                "--exclude", "conversations/*",  # skip gemini conversation logs
                "--no-progress", "--quiet",
            ],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"FAIL {model}/{env}/{task_id}: {result.stderr[:200]}"
        return None
    except subprocess.TimeoutExpired:
        return f"TIMEOUT {model}/{env}/{task_id}"


def _task_already_downloaded(local_dir: Path) -> bool:
    """Check if a task directory already has history.json and at least one screenshot."""
    history = local_dir / "history.json"
    screenshots = local_dir / "screenshots"
    return (
        history.exists()
        and screenshots.exists()
        and any(screenshots.iterdir())
    )


def run_download(workers: int):
    """Phase 1: build manifest and download all successful trajectories."""
    print("Building manifest of successful tasks...")
    manifest = build_manifest()

    # Save manifest
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # Stats
    by_model = defaultdict(int)
    for entry in manifest:
        by_model[entry["model"]] += 1
    print(f"Manifest: {len(manifest)} successful trajectories")
    for model, count in sorted(by_model.items()):
        print(f"  {model}: {count}")

    # Download
    print(f"\nDownloading with {workers} workers...")
    errors = []
    done = 0
    already = 0

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(download_task, e): e for e in manifest}
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                entry = futures[future]
                local_dir = RAW_DIR / entry["model"] / entry["environment"] / entry["task_id"]
                if _task_already_downloaded(local_dir):
                    done += 1
                else:
                    already += 1
            else:
                errors.append(result)
                done += 1

            total = done + already
            if total % 100 == 0:
                print(f"  Progress: {total}/{len(manifest)} ({len(errors)} errors)")

    print(f"\nDownload complete: {done} downloaded, {already} skipped (already present), {len(errors)} errors")
    if errors:
        print("Errors:")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")


# ---------------------------------------------------------------------------
# Phase 2: Upload to HuggingFace Hub
# ---------------------------------------------------------------------------

def run_upload(repo_id: str | None):
    """Upload raw/ directory tree and README directly to HuggingFace Hub."""
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("ERROR: `huggingface_hub` required. Install with: uv pip install huggingface_hub")
        sys.exit(1)

    manifest_path = RAW_DIR / "manifest.json"
    if not manifest_path.exists():
        print("ERROR: manifest.json not found. Run --download first.")
        sys.exit(1)

    api = HfApi()
    user = api.whoami()["name"]

    if repo_id is None:
        repo_id = f"{user}/webarena-infinity-trajectories"

    # Create repo if it doesn't exist
    api.create_repo(repo_id, repo_type="dataset", private=True, exist_ok=True)

    # Print stats before uploading
    manifest = json.loads(manifest_path.read_text())
    by_model = defaultdict(int)
    by_env = defaultdict(int)
    by_diff = defaultdict(int)
    for entry in manifest:
        by_model[entry["model"]] += 1
        by_env[entry["environment"]] += 1
        by_diff[entry["difficulty"]] += 1

    print(f"Dataset: {len(manifest)} successful trajectories")
    print(f"  Models:       {dict(sorted(by_model.items()))}")
    print(f"  Difficulties: {dict(sorted(by_diff.items()))}")
    print(f"  Environments: {len(by_env)}")

    # Upload README first
    readme_path = SCRIPT_DIR / "README.md"
    if readme_path.exists():
        print(f"\nUploading dataset card...")
        api.upload_file(
            path_or_fileobj=str(readme_path),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message="Add dataset card",
        )

    # Upload manifest first
    print(f"\nUploading manifest.json...")
    api.upload_file(
        path_or_fileobj=str(manifest_path),
        path_in_repo="data/manifest.json",
        repo_id=repo_id,
        repo_type="dataset",
        commit_message="Upload manifest",
    )

    # Upload per model to avoid 504 timeouts on large single commits
    for model in MODELS:
        model_dir = RAW_DIR / model
        if not model_dir.exists():
            print(f"  Skipping {model} (not found)")
            continue
        # Upload per environment within each model for even smaller commits
        for env_dir in sorted(model_dir.iterdir()):
            if not env_dir.is_dir():
                continue
            env_name = env_dir.name
            print(f"\nUploading {model}/{env_name}...")
            api.upload_folder(
                folder_path=str(env_dir),
                path_in_repo=f"data/{model}/{env_name}",
                repo_id=repo_id,
                repo_type="dataset",
                commit_message=f"Upload {model}/{env_name} trajectories",
                ignore_patterns=[".DS_Store"],
            )

    print(f"\nDone! Dataset at: https://huggingface.co/datasets/{repo_id}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--download", action="store_true", help="Phase 1: download raw task data from S3")
    parser.add_argument("--upload", action="store_true", help="Phase 2: upload raw data to HuggingFace Hub")
    parser.add_argument("--repo-id", type=str, default=None, help="HF repo id (e.g., user/dataset-name)")
    parser.add_argument("--workers", type=int, default=32, help="Parallel download workers (default: 32)")
    args = parser.parse_args()

    if not args.download and not args.upload:
        parser.print_help()
        sys.exit(1)

    if args.download:
        run_download(args.workers)

    if args.upload:
        run_upload(args.repo_id)


if __name__ == "__main__":
    main()
