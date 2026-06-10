#!/usr/bin/env python3
"""
Docs vs No-Docs Ablation Analysis
==================================
Compares web apps generated with product documentation against those
generated with only a short app description, across 6 dimensions:

1. Functional complexity (distinct operations, entity types, interaction patterns)
2. Task diversity (embedding spread, KNN metrics, clustering)
3. Seed data richness (entity counts, field variety)
4. Verifier complexity (LOC, assertions, state traversal)
5. Task specificity & difficulty calibration
6. Authenticity (feature precision/recall against docs)

Tasks beyond h60 are excluded (hardening artifacts).
Real tasks only for diversity analysis.
Embeddings cached to disk.
"""

import hashlib
import json
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

# ── Configuration ──────────────────────────────────────────────────────────

REPO = Path("/home/ubuntu/mirror-mirror")
APPS_DIR = REPO / "apps"
ABLATIONS_DIR = APPS_DIR / "ablations"
MANUALS_DIR = APPS_DIR / "user-manuals"
OUTPUT_DIR = REPO / "analysis" / "output"
CACHE_DIR = REPO / "analysis" / "cache"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

PAIRS = [
    {
        "name": "elation-prescriptions",
        "docs_app": APPS_DIR / "elation-prescriptions",
        "nodocs_app": ABLATIONS_DIR / "elation-prescriptions-nodocs",
        "docs_path": MANUALS_DIR / "elation" / "prescriptions",
    },
    {
        "name": "figma-slides",
        "docs_app": APPS_DIR / "figma-slides",
        "nodocs_app": ABLATIONS_DIR / "figma-slides-nodocs",
        "docs_path": MANUALS_DIR / "figma" / "figma-slides",
    },
    {
        "name": "gmail-accounts-and-contacts",
        "docs_app": APPS_DIR / "gmail-accounts-and-contacts",
        "nodocs_app": ABLATIONS_DIR / "gmail-accounts-and-contacts-nodocs",
        "docs_path": MANUALS_DIR / "gmail" / "accounts-and-contacts",
    },
    {
        "name": "xero-invoicing",
        "docs_app": APPS_DIR / "xero-invoicing",
        "nodocs_app": ABLATIONS_DIR / "xero-invoicing-nodocs",
        "docs_path": MANUALS_DIR / "xero" / "invoicing",
    },
    {
        "name": "gitlab-plan-and-track",
        "docs_app": APPS_DIR / "gitlab-plan-and-track",
        "nodocs_app": ABLATIONS_DIR / "gitlab-plan-and-track-nodocs",
        "docs_path": MANUALS_DIR / "gitlab" / "topics" / "plan_and_track.md",
    },
]

# Max hard task id to include (exclude hardening artifacts)
MAX_HARD_ID = 60

# ── Gemini Embedding Client (with disk cache) ─────────────────────────────

_client = None
EMBED_MODEL = "gemini-embedding-2-preview"


def get_client():
    global _client
    if _client is None:
        from google import genai
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY")
        _client = genai.Client(api_key=api_key)
    return _client


def _cache_key(text: str, task_type: str) -> str:
    h = hashlib.sha256(f"{task_type}::{text}".encode()).hexdigest()[:16]
    return h


def _load_cache() -> dict[str, list[float]]:
    path = CACHE_DIR / "embeddings.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def _save_cache(cache: dict[str, list[float]]):
    path = CACHE_DIR / "embeddings.json"
    with open(path, "w") as f:
        json.dump(cache, f)


_disk_cache: dict[str, list[float]] | None = None


def embed_texts(texts: list[str], task_type: str = "SEMANTIC_SIMILARITY") -> np.ndarray:
    """Embed texts using Gemini Embedding 2, with persistent disk cache."""
    global _disk_cache
    if _disk_cache is None:
        _disk_cache = _load_cache()

    results: list[tuple[int, list[float]]] = []
    uncached_indices: list[int] = []
    uncached_texts: list[str] = []

    for i, t in enumerate(texts):
        key = _cache_key(t, task_type)
        if key in _disk_cache:
            results.append((i, _disk_cache[key]))
        else:
            uncached_indices.append(i)
            uncached_texts.append(t)

    if uncached_texts:
        print(f"      Cache miss: {len(uncached_texts)}/{len(texts)}, fetching from API...")

    client = get_client() if uncached_texts else None

    BATCH_SIZE = 100
    for batch_start in range(0, len(uncached_texts), BATCH_SIZE):
        batch = uncached_texts[batch_start : batch_start + BATCH_SIZE]
        for attempt in range(5):
            try:
                resp = client.models.embed_content(
                    model=EMBED_MODEL,
                    contents=batch,
                    config={"task_type": task_type},
                )
                break
            except Exception as e:
                if attempt < 4:
                    wait = min(2 ** (attempt + 2), 65)
                    print(f"      Retry {attempt+1}, waiting {wait}s: {e}")
                    time.sleep(wait)
                else:
                    raise

        for j, emb in enumerate(resp.embeddings):
            idx = uncached_indices[batch_start + j]
            vec = emb.values
            key = _cache_key(uncached_texts[batch_start + j], task_type)
            _disk_cache[key] = vec
            results.append((idx, vec))

    # Persist cache after each embed call
    if uncached_texts:
        _save_cache(_disk_cache)

    results.sort(key=lambda x: x[0])
    return np.array([v for _, v in results])


# ── Utility helpers ────────────────────────────────────────────────────────

def read_json(path: Path) -> Any:
    with open(path) as f:
        return json.load(f)


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(errors="replace").splitlines())


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(errors="replace")


def resolve_docs(docs_path: Path) -> str:
    """Resolve docs path (file or dir, possibly with links) into full text."""
    if docs_path.is_file():
        base_dir = docs_path.parent
        entry_text = docs_path.read_text(errors="replace")
        all_texts = [entry_text]
        links = re.findall(r'\(([^)]+\.md)\)', entry_text)
        for link in links:
            target = (base_dir / link).resolve()
            if target.is_file():
                all_texts.append(target.read_text(errors="replace"))
        return "\n\n".join(all_texts)
    elif docs_path.is_dir():
        texts = []
        for md_file in sorted(docs_path.rglob("*.md")):
            texts.append(md_file.read_text(errors="replace"))
        return "\n\n".join(texts)
    return ""


def load_real_tasks(app_dir: Path) -> list[dict]:
    """Load real tasks, excluding hardened tasks (h > MAX_HARD_ID)."""
    path = app_dir / "real-tasks.json"
    if not path.exists():
        return []
    tasks = read_json(path)
    filtered = []
    for t in tasks:
        tid = t["id"]
        # Keep all easy/medium, only keep hard up to MAX_HARD_ID
        if tid.startswith("task_h"):
            num = int(tid.split("_h")[1])
            if num > MAX_HARD_ID:
                continue
        filtered.append(t)
    return filtered


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 1: Functional Complexity
# Uses LLM-extracted features from code (analysis/cache/features/*_code.json)
# ══════════════════════════════════════════════════════════════════════════

def analyze_functionality(name: str, variant: str) -> dict:
    """Dimension 1: Functional complexity from LLM-extracted code features."""
    code_features = load_features(name, f"{variant}_code")
    return {
        "feature_count": len(code_features),
        "features": code_features,
    }


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 2: Task Diversity (Real Tasks Only)
# ══════════════════════════════════════════════════════════════════════════

def compute_diversity_metrics(embeddings: np.ndarray) -> dict:
    """Core diversity metrics from embedding matrix."""
    if len(embeddings) < 2:
        return {}

    dists = cdist(embeddings, embeddings, metric="cosine")
    upper = dists[np.triu_indices_from(dists, k=1)]
    centroid = embeddings.mean(axis=0, keepdims=True)
    centroid_dists = cdist(embeddings, centroid, metric="cosine").flatten()

    return {
        "mean_pairwise_dist": float(np.mean(upper)),
        "median_pairwise_dist": float(np.median(upper)),
        "std_pairwise_dist": float(np.std(upper)),
        "spread": float(np.mean(centroid_dists)),
    }


def compute_knn_metrics(embeddings: np.ndarray, k_values: list[int] = [3, 5, 10]) -> dict:
    """KNN-based diversity metrics."""
    if len(embeddings) < max(k_values) + 1:
        k_values = [k for k in k_values if k < len(embeddings)]
    if not k_values:
        return {}

    results = {}
    nn = NearestNeighbors(metric="cosine")
    nn.fit(embeddings)

    for k in k_values:
        dists, _ = nn.kneighbors(embeddings, n_neighbors=k + 1)
        # Exclude self (column 0)
        knn_dists = dists[:, 1:]
        results[f"knn_{k}_mean"] = float(np.mean(knn_dists[:, -1]))   # distance to k-th neighbor
        results[f"knn_{k}_median"] = float(np.median(knn_dists[:, -1]))
        results[f"knn_{k}_mean_all"] = float(np.mean(knn_dists))      # mean over all k neighbors

    # Coverage: fraction of points that are NOT within eps of any other point
    # (isolated points suggest broader coverage)
    dists_to_nearest = dists[:, 1]  # distance to nearest neighbor
    results["nearest_neighbor_mean"] = float(np.mean(dists_to_nearest))
    results["nearest_neighbor_std"] = float(np.std(dists_to_nearest))
    # Points with nearest neighbor far away (> median) = well-spread
    med = np.median(dists_to_nearest)
    results["pct_isolated_above_median"] = float(np.mean(dists_to_nearest > med) * 100)

    return results


def compute_clustering_metrics(embeddings: np.ndarray) -> dict:
    """Clustering-based diversity metrics."""
    n = len(embeddings)
    if n < 6:
        return {}

    # Find optimal number of clusters via silhouette score
    max_k = min(15, n // 3)
    best_k = 2
    best_score = -1
    scores = {}

    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(embeddings)
        score = silhouette_score(embeddings, labels, metric="cosine")
        scores[k] = score
        if score > best_score:
            best_score = score
            best_k = k

    # Cluster with optimal k
    km = KMeans(n_clusters=best_k, n_init=10, random_state=42)
    labels = km.fit_predict(embeddings)
    cluster_sizes = Counter(labels)
    sizes = sorted(cluster_sizes.values(), reverse=True)

    # Entropy of cluster distribution (higher = more even spread)
    probs = np.array(sizes) / sum(sizes)
    entropy = -np.sum(probs * np.log2(probs + 1e-10))

    return {
        "optimal_k": best_k,
        "silhouette_score": float(best_score),
        "cluster_sizes": sizes,
        "cluster_entropy": float(entropy),
        "largest_cluster_pct": float(sizes[0] / n * 100),
        "smallest_cluster_pct": float(sizes[-1] / n * 100),
    }


def compute_cross_overlap(embs_a: np.ndarray, embs_b: np.ndarray) -> dict:
    """Measure overlap between two task sets."""
    if len(embs_a) == 0 or len(embs_b) == 0:
        return {}

    cross_dists = cdist(embs_a, embs_b, metric="cosine")
    nn_a_to_b = cross_dists.min(axis=1)
    nn_b_to_a = cross_dists.min(axis=0)

    return {
        "mean_cross_dist": float(np.mean(cross_dists)),
        "nn_a_to_b_mean": float(np.mean(nn_a_to_b)),
        "nn_b_to_a_mean": float(np.mean(nn_b_to_a)),
        "nn_symmetric_mean": float((np.mean(nn_a_to_b) + np.mean(nn_b_to_a)) / 2),
    }


def analyze_task_diversity(docs_app: Path, nodocs_app: Path) -> dict:
    """Dimension 2: Real task diversity via embeddings (KNN + clustering)."""
    docs_tasks = load_real_tasks(docs_app)
    nodocs_tasks = load_real_tasks(nodocs_app)

    docs_instructions = [t["instruction"] for t in docs_tasks]
    nodocs_instructions = [t["instruction"] for t in nodocs_tasks]

    all_instructions = docs_instructions + nodocs_instructions
    if not all_instructions:
        return {}

    print(f"    Embedding {len(all_instructions)} real task instructions...")
    all_embs = embed_texts(all_instructions)

    docs_embs = all_embs[: len(docs_instructions)]
    nodocs_embs = all_embs[len(docs_instructions) :]

    results = {
        "docs_count": len(docs_tasks),
        "nodocs_count": len(nodocs_tasks),
    }

    # Core diversity
    if len(docs_embs) > 1:
        results["docs_diversity"] = compute_diversity_metrics(docs_embs)
        results["docs_knn"] = compute_knn_metrics(docs_embs)
        results["docs_clustering"] = compute_clustering_metrics(docs_embs)
    if len(nodocs_embs) > 1:
        results["nodocs_diversity"] = compute_diversity_metrics(nodocs_embs)
        results["nodocs_knn"] = compute_knn_metrics(nodocs_embs)
        results["nodocs_clustering"] = compute_clustering_metrics(nodocs_embs)

    # Cross-set overlap
    if len(docs_embs) > 0 and len(nodocs_embs) > 0:
        results["cross_overlap"] = compute_cross_overlap(docs_embs, nodocs_embs)

    # Store for visualization
    results["docs_embs"] = docs_embs
    results["nodocs_embs"] = nodocs_embs
    results["docs_instructions"] = docs_instructions
    results["nodocs_instructions"] = nodocs_instructions

    return results


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 3: Seed Data Richness
# ══════════════════════════════════════════════════════════════════════════

def analyze_js_data(app_dir: Path) -> dict:
    """Dimension 3: Analyze seed data richness from data.js."""
    data_path = app_dir / "js" / "data.js"
    text = read_text(data_path)
    if not text:
        return {"loc": 0, "arrays": 0, "total_entities": 0, "unique_string_values": 0}

    loc = len(text.splitlines())

    array_defs = re.findall(r'(?:const|let|var)\s+\w+\s*=\s*\[', text)
    array_props = re.findall(r'\w+\s*:\s*\[', text)
    array_count = len(array_defs) + len(array_props)

    entity_matches = re.findall(r'\{\s*\n?\s*\w+\s*:', text)
    entity_count = len(entity_matches)

    string_values = re.findall(r'["\']([^"\']{2,})["\']', text)
    unique_strings = set(string_values)

    field_names = set(re.findall(r'(\w+)\s*:', text))
    js_keywords = {'function', 'return', 'const', 'let', 'var', 'if', 'else', 'for',
                   'while', 'switch', 'case', 'break', 'default', 'true', 'false',
                   'null', 'undefined', 'new', 'this', 'class', 'export', 'import'}
    field_names -= js_keywords

    emails = set(re.findall(r'[\w.-]+@[\w.-]+\.\w+', text))
    dates = set(re.findall(r'\d{4}-\d{2}-\d{2}', text))

    return {
        "loc": loc,
        "array_collections": array_count,
        "total_entities": entity_count,
        "unique_fields": len(field_names),
        "unique_string_values": len(unique_strings),
        "total_string_values": len(string_values),
        "unique_emails": len(emails),
        "unique_dates": len(dates),
    }


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 4: Verifier Complexity
# ══════════════════════════════════════════════════════════════════════════

def analyze_verifier(path: Path) -> dict:
    text = read_text(path)
    loc = len(text.splitlines())

    assert_patterns = [
        r'\bassert\b', r'\bif\s+not\b', r'\bif\s+\w',
        r'==\s', r'!=\s', r'\bnot\s+in\b',
    ]
    assertions = sum(len(re.findall(p, text)) for p in assert_patterns)

    bracket_chains = re.findall(r'(?:\[[\"\'][^\]]+[\"\']\])+', text)
    max_depth = max((s.count('[') for s in bracket_chains), default=0)

    state_keys = set(re.findall(r'[\["\'](\w+)[\]"\']', text))
    has_loops = bool(re.search(r'\bfor\b.*\bin\b', text))
    fn_defs = len(re.findall(r'\bdef\s+\w+', text))

    return {
        "loc": loc,
        "assertion_count": assertions,
        "max_state_depth": max_depth,
        "unique_state_keys": len(state_keys),
        "has_loops": has_loops,
        "helper_functions": fn_defs,
    }


def analyze_verifiers(app_dir: Path) -> dict:
    """Dimension 4: Aggregate verifier complexity (real tasks only, ≤ h60)."""
    task_dir = app_dir / "real-tasks"
    if not task_dir.exists():
        return {}

    verifiers = []
    for v in sorted(task_dir.glob("task_*.py")):
        # Filter out hardened tasks
        name = v.stem  # e.g., task_h61
        if name.startswith("task_h"):
            num = int(name.split("_h")[1])
            if num > MAX_HARD_ID:
                continue
        verifiers.append(v)

    if not verifiers:
        return {}

    metrics = [analyze_verifier(v) for v in verifiers]
    locs = [m["loc"] for m in metrics]
    asserts = [m["assertion_count"] for m in metrics]
    depths = [m["max_state_depth"] for m in metrics]
    keys = [m["unique_state_keys"] for m in metrics]
    loops = [m["has_loops"] for m in metrics]
    fns = [m["helper_functions"] for m in metrics]

    return {
        "count": len(verifiers),
        "loc_mean": float(np.mean(locs)),
        "loc_median": float(np.median(locs)),
        "loc_total": sum(locs),
        "assertions_mean": float(np.mean(asserts)),
        "max_depth_mean": float(np.mean(depths)),
        "state_keys_mean": float(np.mean(keys)),
        "pct_with_loops": float(np.mean(loops) * 100),
        "helper_fns_mean": float(np.mean(fns)),
    }


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 5: Task Specificity & Difficulty Calibration
# ══════════════════════════════════════════════════════════════════════════

def analyze_task_specificity(app_dir: Path) -> dict:
    """Dimension 5: Task instruction analysis (real tasks, ≤ h60)."""
    tasks = load_real_tasks(app_dir)
    if not tasks:
        return {}

    instructions = [t["instruction"] for t in tasks]
    word_counts = [len(inst.split()) for inst in instructions]

    by_difficulty = defaultdict(list)
    for t in tasks:
        by_difficulty[t.get("difficulty", "unknown")].append(len(t["instruction"].split()))

    entity_refs = []
    for inst in instructions:
        named = re.findall(r'(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+|[A-Z]+-\d+|\b[A-Z]{2,}\b)', inst)
        entity_refs.append(len(named))

    first_words = Counter(inst.split()[0].lower() for inst in instructions if inst)

    results = {
        "count": len(tasks),
        "word_count_mean": float(np.mean(word_counts)),
        "word_count_median": float(np.median(word_counts)),
        "word_count_std": float(np.std(word_counts)),
        "entity_refs_mean": float(np.mean(entity_refs)),
        "entity_refs_pct": float(sum(1 for e in entity_refs if e > 0) / len(entity_refs) * 100),
        "top_verbs": dict(first_words.most_common(10)),
    }

    for diff in ["easy", "medium", "hard"]:
        if diff in by_difficulty:
            results[f"{diff}_word_count_mean"] = float(np.mean(by_difficulty[diff]))
            results[f"{diff}_count"] = len(by_difficulty[diff])

    return results


# ══════════════════════════════════════════════════════════════════════════
# DIMENSION 6: Authenticity (Feature Precision/Recall vs Docs)
# Uses LLM-extracted features from analysis/cache/features/
# Run analysis/extract_features.py first to populate the cache.
# ══════════════════════════════════════════════════════════════════════════

FEATURE_CACHE = REPO / "analysis" / "cache" / "features"
AUTH_THRESHOLD = 0.20  # cosine distance threshold for feature match


def load_features(name: str, variant: str) -> list[str]:
    """Load LLM-extracted features from cache."""
    path = FEATURE_CACHE / f"{name}_{variant}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Feature cache missing: {path}\n"
            f"Run: python analysis/extract_features.py"
        )
    with open(path) as f:
        return json.load(f)


def compute_authenticity(name: str) -> dict:
    """Dimension 6: Feature precision/recall against docs using LLM-extracted features."""
    doc_features = load_features(name, "docs")
    docs_app_features = load_features(name, "docs_app")
    nodocs_app_features = load_features(name, "nodocs_app")

    print(f"    Doc features: {len(doc_features)}, "
          f"Docs-app: {len(docs_app_features)}, "
          f"Nodocs-app: {len(nodocs_app_features)}")

    all_features = doc_features + docs_app_features + nodocs_app_features
    print(f"    Embedding {len(all_features)} feature phrases...")
    all_embs = embed_texts(all_features, task_type="SEMANTIC_SIMILARITY")

    n_doc = len(doc_features)
    n_docs_app = len(docs_app_features)

    doc_embs = all_embs[:n_doc]
    docs_app_embs = all_embs[n_doc : n_doc + n_docs_app]
    nodocs_app_embs = all_embs[n_doc + n_docs_app :]

    def precision_recall(app_embs, app_features, label):
        if len(app_embs) == 0 or len(doc_embs) == 0:
            return {}
        cross = cdist(app_embs, doc_embs, metric="cosine")
        app_to_doc_nn = cross.min(axis=1)
        precision = float(np.mean(app_to_doc_nn < AUTH_THRESHOLD))

        doc_to_app_nn = cross.min(axis=0)
        recall = float(np.mean(doc_to_app_nn < AUTH_THRESHOLD))

        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return {
            f"{label}_precision": precision,
            f"{label}_recall": recall,
            f"{label}_f1": f1,
            f"{label}_mean_dist_to_docs": float(np.mean(app_to_doc_nn)),
            f"{label}_feature_count": len(app_features),
        }

    results = {"doc_feature_count": n_doc}
    results.update(precision_recall(docs_app_embs, docs_app_features, "docs_app"))
    results.update(precision_recall(nodocs_app_embs, nodocs_app_features, "nodocs_app"))
    return results


# ══════════════════════════════════════════════════════════════════════════
# VISUALIZATION
# ══════════════════════════════════════════════════════════════════════════

DOCS_COLOR = "#77B1F2"     # Soft blue
NODOCS_COLOR = "#F08D8D"   # Soft red

# Apply style guide rcParams globally
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

SAVE_DPI = 300


def short_name(name: str) -> str:
    return name.replace("-", "\n")


def plot_dimension1(all_results: dict, output_dir: Path):
    """Functional complexity: distinct capabilities extracted from code."""
    app_names = [p["name"] for p in PAIRS]
    x = np.arange(len(app_names))
    width = 0.35

    docs_vals = [all_results[name]["func_docs"]["feature_count"] for name in app_names]
    nodocs_vals = [all_results[name]["func_nodocs"]["feature_count"] for name in app_names]

    fig, ax = plt.subplots(figsize=(6, 3.2))

    ax.bar(x - width/2, docs_vals, width, label="With Docs", color=DOCS_COLOR,
           edgecolor="white", linewidth=0.5)
    ax.bar(x + width/2, nodocs_vals, width, label="No Docs", color=NODOCS_COLOR,
           edgecolor="white", linewidth=0.5)

    for i, (dv, nv) in enumerate(zip(docs_vals, nodocs_vals)):
        ax.text(i - width/2, dv + 1, str(dv), ha="center", va="bottom", fontsize=9)
        ax.text(i + width/2, nv + 1, str(nv), ha="center", va="bottom", fontsize=9)

    # Headroom so labels don't collide with top spine
    ax.set_ylim(0, max(max(docs_vals), max(nodocs_vals)) * 1.15)
    ax.set_title("Functional complexity of generated environments")
    ax.set_ylabel("Distinct capabilities")
    ax.set_xticks(x)
    ax.set_xticklabels([short_name(n) for n in app_names])
    # Legend omitted — shown on dim2 (right panel) when displayed side-by-side

    fig.savefig(output_dir / "dim1_functionality.png", dpi=SAVE_DPI, bbox_inches="tight")
    plt.close(fig)
    print("  Saved dim1_functionality.png")


def plot_dimension2(all_results: dict, output_dir: Path):
    """Task diversity: 5-NN distance comparison."""
    app_names = [p["name"] for p in PAIRS]

    docs_vals = []
    nodocs_vals = []
    valid_names = []
    for name in app_names:
        d = all_results[name]["diversity"]
        dk, nk = "docs_knn", "nodocs_knn"
        if dk in d and nk in d and "knn_5_mean" in d[dk] and "knn_5_mean" in d[nk]:
            docs_vals.append(d[dk]["knn_5_mean"])
            nodocs_vals.append(d[nk]["knn_5_mean"])
            valid_names.append(name)

    x = np.arange(len(valid_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6, 3.2))

    ax.bar(x - width/2, docs_vals, width, label="With Docs", color=DOCS_COLOR,
           edgecolor="white", linewidth=0.5)
    ax.bar(x + width/2, nodocs_vals, width, label="No Docs", color=NODOCS_COLOR,
           edgecolor="white", linewidth=0.5)

    for i, (dv, nv) in enumerate(zip(docs_vals, nodocs_vals)):
        ax.text(i - width/2, dv + 0.002, f"{dv:.2f}", ha="center", va="bottom", fontsize=9)
        ax.text(i + width/2, nv + 0.002, f"{nv:.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylim(0, max(max(docs_vals), max(nodocs_vals)) * 1.15)
    ax.set_title("Task diversity across generated environments")
    ax.set_ylabel("5-NN cosine distance")
    ax.set_xticks(x)
    ax.set_xticklabels([short_name(n) for n in valid_names])
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 0.15),
              frameon=True, framealpha=0.9, edgecolor='#DDD')

    fig.savefig(output_dir / "dim2_diversity_metrics.png", dpi=SAVE_DPI, bbox_inches="tight")
    plt.close(fig)
    print("  Saved dim2 plots")


def plot_dimension3(all_results: dict, output_dir: Path):
    """Seed data richness."""
    app_names = [p["name"] for p in PAIRS]
    x = np.arange(len(app_names))
    width = 0.35

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Dimension 3: Seed Data Richness", fontsize=16, fontweight="bold")

    metrics = [
        ("loc", "data.js LOC"),
        ("total_entities", "Total Entities"),
        ("unique_fields", "Unique Fields"),
        ("unique_string_values", "Unique String Values"),
        ("array_collections", "Array Collections"),
        ("unique_dates", "Unique Date Values"),
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 3][idx % 3]
        docs_vals = [all_results[name]["data_docs"].get(metric, 0) for name in app_names]
        nodocs_vals = [all_results[name]["data_nodocs"].get(metric, 0) for name in app_names]

        ax.bar(x - width/2, docs_vals, width, label="With Docs", color=DOCS_COLOR, alpha=0.85)
        ax.bar(x + width/2, nodocs_vals, width, label="No Docs", color=NODOCS_COLOR, alpha=0.85)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels([short_name(n) for n in app_names], fontsize=7)
        ax.legend(fontsize=8)

    plt.tight_layout()
    fig.savefig(output_dir / "dim3_data_richness.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved dim3_data_richness.png")


def plot_dimension4(all_results: dict, output_dir: Path):
    """Verifier complexity."""
    app_names = [p["name"] for p in PAIRS]
    x = np.arange(len(app_names))
    width = 0.35

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Dimension 4: Verifier Complexity", fontsize=16, fontweight="bold")

    metrics = [
        ("loc_mean", "Mean LOC / Verifier"),
        ("assertions_mean", "Mean Assertions"),
        ("max_depth_mean", "Mean State Depth"),
        ("state_keys_mean", "Mean State Keys"),
        ("pct_with_loops", "% With Loops"),
        ("helper_fns_mean", "Mean Helper Functions"),
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 3][idx % 3]
        docs_vals = [all_results[name]["verifiers_docs"].get(metric, 0) for name in app_names]
        nodocs_vals = [all_results[name]["verifiers_nodocs"].get(metric, 0) for name in app_names]

        ax.bar(x - width/2, docs_vals, width, label="With Docs", color=DOCS_COLOR, alpha=0.85)
        ax.bar(x + width/2, nodocs_vals, width, label="No Docs", color=NODOCS_COLOR, alpha=0.85)
        ax.set_title(title, fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels([short_name(n) for n in app_names], fontsize=7)
        ax.legend(fontsize=8)

    plt.tight_layout()
    fig.savefig(output_dir / "dim4_verifier_complexity.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved dim4_verifier_complexity.png")


def plot_dimension5(all_results: dict, output_dir: Path):
    """Task specificity and difficulty calibration."""
    app_names = [p["name"] for p in PAIRS]

    # Instruction length by difficulty
    fig, axes = plt.subplots(1, len(app_names), figsize=(4 * len(app_names), 5))
    fig.suptitle("Dimension 5: Task Instruction Length by Difficulty", fontsize=16, fontweight="bold")

    for i, name in enumerate(app_names):
        ax = axes[i]
        docs_spec = all_results[name]["specificity_docs"]
        nodocs_spec = all_results[name]["specificity_nodocs"]

        diffs = ["easy", "medium", "hard"]
        docs_means = [docs_spec.get(f"{d}_word_count_mean", 0) for d in diffs]
        nodocs_means = [nodocs_spec.get(f"{d}_word_count_mean", 0) for d in diffs]

        xx = np.arange(len(diffs))
        width = 0.35
        ax.bar(xx - width/2, docs_means, width, label="With Docs", color=DOCS_COLOR, alpha=0.85)
        ax.bar(xx + width/2, nodocs_means, width, label="No Docs", color=NODOCS_COLOR, alpha=0.85)
        ax.set_title(short_name(name), fontsize=9)
        ax.set_xticks(xx)
        ax.set_xticklabels(diffs)
        ax.set_ylabel("Mean Words" if i == 0 else "")
        if i == 0:
            ax.legend(fontsize=8)

    plt.tight_layout()
    fig.savefig(output_dir / "dim5_difficulty_calibration.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Entity reference rate
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle("Dimension 5: Entity Reference Rate in Task Instructions", fontsize=14, fontweight="bold")

    docs_rates = [all_results[name]["specificity_docs"].get("entity_refs_pct", 0) for name in app_names]
    nodocs_rates = [all_results[name]["specificity_nodocs"].get("entity_refs_pct", 0) for name in app_names]

    x = np.arange(len(app_names))
    width = 0.35
    ax.bar(x - width/2, docs_rates, width, label="With Docs", color=DOCS_COLOR, alpha=0.85)
    ax.bar(x + width/2, nodocs_rates, width, label="No Docs", color=NODOCS_COLOR, alpha=0.85)
    ax.set_ylabel("% of Tasks with Named Entities")
    ax.set_xticks(x)
    ax.set_xticklabels([short_name(n) for n in app_names], fontsize=8)
    ax.legend()

    plt.tight_layout()
    fig.savefig(output_dir / "dim5_entity_refs.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved dim5 plots")


def plot_dimension6(all_results: dict, output_dir: Path):
    """Authenticity: precision and recall bar plots side by side."""
    app_names = [p["name"] for p in PAIRS]
    x = np.arange(len(app_names))
    width = 0.35

    fig, (ax_p, ax_r) = plt.subplots(1, 2, figsize=(11, 3.2))

    for ax, metric, title in [
        (ax_p, "precision", "Precision"),
        (ax_r, "recall", "Recall"),
    ]:
        docs_vals = []
        nodocs_vals = []
        for name in app_names:
            auth = all_results[name].get("authenticity", {})
            docs_vals.append(auth.get(f"docs_app_{metric}", 0))
            nodocs_vals.append(auth.get(f"nodocs_app_{metric}", 0))

        ax.bar(x - width/2, docs_vals, width, label="With Docs", color=DOCS_COLOR,
               edgecolor="white", linewidth=0.5)
        ax.bar(x + width/2, nodocs_vals, width, label="No Docs", color=NODOCS_COLOR,
               edgecolor="white", linewidth=0.5)

        for i, (dv, nv) in enumerate(zip(docs_vals, nodocs_vals)):
            ax.text(i - width/2, dv + 0.01, f"{dv:.2f}", ha="center", va="bottom", fontsize=9)
            ax.text(i + width/2, nv + 0.01, f"{nv:.2f}", ha="center", va="bottom", fontsize=9)

        ymax = max(max(docs_vals), max(nodocs_vals))
        ax.set_ylim(0, min(ymax * 1.18, 1.0))
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels([short_name(n) for n in app_names])

    fig.legend(*ax_r.get_legend_handles_labels(),
               loc="lower right", bbox_to_anchor=(0.98, 0.02),
               frameon=True, framealpha=0.9, edgecolor='#DDD')

    fig.suptitle("Feature authenticity of generated environments", y=1.02)
    fig.savefig(output_dir / "dim6_authenticity.png", dpi=SAVE_DPI)
    plt.close(fig)
    print("  Saved dim6_authenticity.png")


# ══════════════════════════════════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════════════════════════════════

def generate_summary_report(all_results: dict, output_dir: Path):
    app_names = [p["name"] for p in PAIRS]
    lines = [
        "# Docs vs No-Docs Ablation Analysis",
        "",
        f"**Generated**: {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Apps analyzed**: {len(PAIRS)}",
        f"**Task filter**: real tasks only, hard tasks ≤ h{MAX_HARD_ID}",
        "",
    ]

    # Dim 1
    lines += [
        "## Dimension 1: Functional Complexity (LLM-extracted from code)",
        "",
        "| App | With Docs | No Docs |",
        "|-----|----------|---------|",
    ]
    for name in app_names:
        d = all_results[name]["func_docs"]["feature_count"]
        n = all_results[name]["func_nodocs"]["feature_count"]
        lines.append(f"| {name} | {d} | {n} |")
    lines.append("")

    # Dim 2
    lines += [
        "## Dimension 2: Task Diversity (Real Tasks)",
        "",
        "| App | | Count | Mean Pairwise | 5-NN Dist | Optimal K | Cluster Entropy | Silhouette |",
        "|-----|---|-------|--------------|----------|----------|----------------|-----------|",
    ]
    for name in app_names:
        d = all_results[name]["diversity"]
        for label, prefix in [("Docs", "docs"), ("NoDocs", "nodocs")]:
            div = d.get(f"{prefix}_diversity", {})
            knn = d.get(f"{prefix}_knn", {})
            clust = d.get(f"{prefix}_clustering", {})
            count = d.get(f"{prefix}_count", 0)
            lines.append(
                f"| {name if label == 'Docs' else ''} | {label} | {count} | "
                f"{div.get('mean_pairwise_dist', 0):.4f} | "
                f"{knn.get('knn_5_mean', 0):.4f} | "
                f"{clust.get('optimal_k', 0)} | "
                f"{clust.get('cluster_entropy', 0):.2f} | "
                f"{clust.get('silhouette_score', 0):.3f} |"
            )
    lines.append("")

    # Dim 3
    lines += [
        "## Dimension 3: Seed Data Richness",
        "",
        "| App | | data.js LOC | Entities | Unique Fields | Unique Strings |",
        "|-----|---|------------|----------|--------------|----------------|",
    ]
    for name in app_names:
        d = all_results[name]["data_docs"]
        n = all_results[name]["data_nodocs"]
        lines.append(f"| {name} | Docs | {d['loc']} | {d['total_entities']} | {d['unique_fields']} | {d['unique_string_values']} |")
        lines.append(f"| | NoDocs | {n['loc']} | {n['total_entities']} | {n['unique_fields']} | {n['unique_string_values']} |")
    lines.append("")

    # Dim 4
    lines += [
        "## Dimension 4: Verifier Complexity",
        "",
        "| App | | Mean LOC | Mean Assertions | Mean State Depth | % With Loops |",
        "|-----|---|---------|----------------|-----------------|-------------|",
    ]
    for name in app_names:
        d = all_results[name]["verifiers_docs"]
        n = all_results[name]["verifiers_nodocs"]
        lines.append(
            f"| {name} | Docs | {d.get('loc_mean', 0):.1f} | {d.get('assertions_mean', 0):.1f} | "
            f"{d.get('max_depth_mean', 0):.1f} | {d.get('pct_with_loops', 0):.0f}% |"
        )
        lines.append(
            f"| | NoDocs | {n.get('loc_mean', 0):.1f} | {n.get('assertions_mean', 0):.1f} | "
            f"{n.get('max_depth_mean', 0):.1f} | {n.get('pct_with_loops', 0):.0f}% |"
        )
    lines.append("")

    # Dim 5
    lines += [
        "## Dimension 5: Task Specificity & Difficulty Calibration",
        "",
        "| App | | Count | Mean Words | Entity Ref % | Easy | Medium | Hard |",
        "|-----|---|-------|-----------|-------------|------|--------|------|",
    ]
    for name in app_names:
        d = all_results[name]["specificity_docs"]
        n = all_results[name]["specificity_nodocs"]
        lines.append(
            f"| {name} | Docs | {d.get('count', 0)} | {d.get('word_count_mean', 0):.1f} | {d.get('entity_refs_pct', 0):.0f}% | "
            f"{d.get('easy_word_count_mean', 0):.1f} | {d.get('medium_word_count_mean', 0):.1f} | {d.get('hard_word_count_mean', 0):.1f} |"
        )
        lines.append(
            f"| | NoDocs | {n.get('count', 0)} | {n.get('word_count_mean', 0):.1f} | {n.get('entity_refs_pct', 0):.0f}% | "
            f"{n.get('easy_word_count_mean', 0):.1f} | {n.get('medium_word_count_mean', 0):.1f} | {n.get('hard_word_count_mean', 0):.1f} |"
        )
    lines.append("")

    # Dim 6
    lines += [
        "## Dimension 6: Authenticity (Feature Precision/Recall vs Docs)",
        "",
        "| App | | Precision | Recall | F1 | Feature Count |",
        "|-----|---|----------|--------|-----|--------------|",
    ]
    for name in app_names:
        auth = all_results[name].get("authenticity", {})
        lines.append(
            f"| {name} | Docs | {auth.get('docs_app_precision', 0):.3f} | {auth.get('docs_app_recall', 0):.3f} | "
            f"{auth.get('docs_app_f1', 0):.3f} | {auth.get('docs_app_feature_count', 0)} |"
        )
        lines.append(
            f"| | NoDocs | {auth.get('nodocs_app_precision', 0):.3f} | {auth.get('nodocs_app_recall', 0):.3f} | "
            f"{auth.get('nodocs_app_f1', 0):.3f} | {auth.get('nodocs_app_feature_count', 0)} |"
        )
    lines.append("")

    report = "\n".join(lines)
    (output_dir / "report.md").write_text(report)
    print(f"\n  Report saved to {output_dir / 'report.md'}")
    return report


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("Docs vs No-Docs Ablation Analysis")
    print(f"  Task filter: real tasks only, hard ≤ h{MAX_HARD_ID}")
    print("=" * 70)

    all_results = {}

    for pair in PAIRS:
        name = pair["name"]
        docs_app = pair["docs_app"]
        nodocs_app = pair["nodocs_app"]
        docs_path = pair["docs_path"]

        print(f"\n{'─' * 50}")
        print(f"Analyzing: {name}")
        print(f"{'─' * 50}")

        result = {}

        print("  [1/6] Functional complexity (LLM-extracted code features)...")
        result["func_docs"] = analyze_functionality(name, "docs_app")
        result["func_nodocs"] = analyze_functionality(name, "nodocs_app")

        print("  [2/6] Task diversity (embeddings + KNN + clustering)...")
        result["diversity"] = analyze_task_diversity(docs_app, nodocs_app)

        print("  [3/6] Seed data richness...")
        result["data_docs"] = analyze_js_data(docs_app)
        result["data_nodocs"] = analyze_js_data(nodocs_app)

        print("  [4/6] Verifier complexity...")
        result["verifiers_docs"] = analyze_verifiers(docs_app)
        result["verifiers_nodocs"] = analyze_verifiers(nodocs_app)

        print("  [5/6] Task specificity...")
        result["specificity_docs"] = analyze_task_specificity(docs_app)
        result["specificity_nodocs"] = analyze_task_specificity(nodocs_app)

        print("  [6/6] Authenticity (LLM-extracted features, threshold=0.20)...")
        result["authenticity"] = compute_authenticity(name)

        all_results[name] = result

    print(f"\n{'=' * 50}")
    print("Generating visualizations...")
    print(f"{'=' * 50}")

    plot_dimension1(all_results, OUTPUT_DIR)
    plot_dimension2(all_results, OUTPUT_DIR)
    plot_dimension3(all_results, OUTPUT_DIR)
    plot_dimension4(all_results, OUTPUT_DIR)
    plot_dimension5(all_results, OUTPUT_DIR)
    plot_dimension6(all_results, OUTPUT_DIR)

    report = generate_summary_report(all_results, OUTPUT_DIR)

    # Save raw results (skip numpy arrays)
    def make_serializable(obj):
        if isinstance(obj, np.ndarray):
            return None
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        return obj

    raw_path = OUTPUT_DIR / "raw_results.json"
    with open(raw_path, "w") as f:
        json.dump(make_serializable(all_results), f, indent=2, default=str)
    print(f"  Raw results saved to {raw_path}")

    print(f"\n{'=' * 70}")
    print("DONE — all outputs in:", OUTPUT_DIR)
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
