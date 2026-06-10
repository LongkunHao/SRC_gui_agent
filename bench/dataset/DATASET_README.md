---
license: mit
task_categories:
  - visual-question-answering
  - image-to-text
tags:
  - browser-agent
  - web-navigation
  - trajectories
  - gui-grounding
pretty_name: "WebArena-Infinity: Browser Agent Trajectories"
size_categories:
  - 1K<n<10K
---

# WebArena-Infinity: Browser Agent Trajectories

Successful browser-agent trajectories collected from the WebArena-Infinity evaluation benchmark. Each trajectory records a browser agent completing a real web-application task — including step-by-step screenshots (raw, no overlays), agent reasoning, and actions.

## Dataset Summary

| | Gemini-3-Flash | Kimi-K2.5 | Qwen-3.5-Plus | Total |
|---|---|---|---|---|
| Trajectories | ~870 | ~580 | ~620 | ~2,070 |
| Environments | 13 | 13 | 13 | 13 |

Trajectories span 13 auto-generated web-application environments sourced from real product documentation (Gmail, GitLab, PayPal, Xero, Elation EHR, Superhuman, Handshake, Linear, Figma).

## Schema

Each row is one complete trajectory (one agent solving one task):

| Column | Type | Description |
|---|---|---|
| `trajectory_id` | `string` | Unique ID: `{model}_{environment}_{task_id}` |
| `model` | `string` | Agent model: `gemini`, `kimi`, or `qwen` |
| `environment` | `string` | Web-app environment name |
| `task_id` | `string` | Task identifier (e.g., `task_e1`, `task_m5`, `task_h3`) |
| `difficulty` | `string` | `easy`, `medium`, or `hard` |
| `instruction` | `string` | Natural-language task instruction given to the agent |
| `num_steps` | `int32` | Number of agent steps taken |
| `elapsed_seconds` | `float64` | Wall-clock time to complete the task |
| `agent_format` | `string` | `browser_use` or `vision_agent` (see below) |
| `source_run` | `string` | Which repetition this trajectory came from (`run1`, `run2`, `run3`) |
| `history` | `string` | JSON-encoded list of steps, each with `thought` and `actions` |
| `screenshots` | `Sequence(Image)` | Ordered list of screenshots, one per step (PNG, raw, no overlay) |
| `verifier_message` | `string` | Message from the programmatic verifier confirming success |

## Agent Formats

The `history` column stores the original agent output format — **not** normalized across models. The `agent_format` field tells you which format to expect.

### `browser_use` (Gemini-3-Flash)

Gemini uses the [Browser Use](https://github.com/browser-use/browser-use) harness, which interacts via DOM element indices (not pixel coordinates). It receives a text-based accessibility representation of the page.

```json
{
  "thought": "Evaluation: The star button was clicked...\nMemory: James O'Brien at index 2072...\nGoal: Signal completion.",
  "actions": [{"click": {"index": 1177}}],
  "state": {"url": "http://...", "title": "..."},
  "metadata": {"step_number": 1, "step_start_time": ..., "step_end_time": ...}
}
```

**Fields in each step:**
- `thought` — Concatenation of the model's `evaluation_previous_goal`, `memory`, and `next_goal` fields
- `actions` — List of Browser Use action dicts. Action types include `click`, `navigate`, `input_text`, `scroll_down`, `scroll_up`, `done`, etc. The `click` and `input_text` actions reference DOM elements by `index` (an integer assigned by Browser Use to each interactive element on the page)
- `state` — Page state at this step (URL, title, tab info)
- `metadata` — Timing info (step number, start/end timestamps)

### `vision_agent` (Kimi-K2.5, Qwen-3.5-Plus)

Kimi and Qwen are vision-based agents that interact via pixel coordinates on screenshots. They receive a screenshot as input and output click/type/scroll actions at specific (x, y) positions.

```json
{
  "thought": "Click on the star icon next to Sarah Chen's email to star it.\n## Code:\n```python\npyautogui.click(x=0.018, y=0.175)\n```",
  "actions": [{"type": "click", "x": 35, "y": 189}]
}
```

**Fields in each step:**
- `thought` — Free-form reasoning from the agent, including what it observed and why it chose the action. Kimi includes `pyautogui` code snippets; Qwen includes `<tool_call>` XML blocks. Both are part of the raw model output.
- `actions` — List of action dicts with `type` (`click`, `type`, `scroll`, `terminate`) and pixel coordinates `x`, `y` (absolute pixels on the screenshot).

### Key differences at a glance

| | `browser_use` (Gemini) | `vision_agent` (Kimi/Qwen) |
|---|---|---|
| Input modality | Text (DOM tree) | Vision (screenshot) |
| Action targeting | DOM element index | Pixel coordinates (x, y) |
| Thought structure | Structured (eval + memory + goal) | Free-form text |
| Extra fields | `state`, `metadata` | — |

## Environments

| Environment | Domain | Source | Tasks |
|---|---|---|---|
| `elation-clinical-records` | Healthcare | Elation EHR | 120 |
| `elation-patient-communication` | Healthcare | Elation EHR | 120 |
| `elation-prescriptions` | Healthcare | Elation EHR | 120 |
| `figma-slides` | Design | Figma | 120 |
| `figma-text-and-typography` | Design | Figma | 120 |
| `gitlab-plan-and-track` | DevOps | GitLab | 140 |
| `gmail` | Productivity | Gmail | 60 |
| `gmail-accounts-and-contacts` | Productivity | Gmail | 120 |
| `handshake-career-exploration` | Careers | Handshake | 200 |
| `linear-account-settings` | Project Mgmt | Linear | 120 |
| `paypal-my-wallet` | Finance | PayPal | 140 |
| `superhuman-general` | Productivity | Superhuman | 120 |
| `xero-invoicing` | Finance | Xero | 120 |

## How to use

```python
from datasets import load_dataset
import json

ds = load_dataset("webarena-x/webarena-infinity-trajectories")

# Get one trajectory
traj = ds["train"][0]
print(traj["instruction"])
print(f"{traj['num_steps']} steps, {traj['elapsed_seconds']:.1f}s")

# Parse history
history = json.loads(traj["history"])
for i, step in enumerate(history):
    print(f"Step {i}: {step['thought'][:100]}...")
    print(f"  Actions: {step['actions']}")

# Access screenshots
for i, img in enumerate(traj["screenshots"]):
    img.save(f"step_{i}.png")
```

### Filtering by agent format

```python
# Vision-agent trajectories only (Kimi + Qwen)
vision_ds = ds["train"].filter(lambda x: x["agent_format"] == "vision_agent")

# Gemini trajectories only
gemini_ds = ds["train"].filter(lambda x: x["model"] == "gemini")
```

## Construction

This dataset was built from the [WebArena-Infinity](https://github.com/web-arena-x/webarena-infinity) evaluation pipeline. Each trajectory represents a successful task completion from a 3-repetition final evaluation run. For tasks that succeeded in multiple repetitions, the merged result selects one canonical trajectory (typically from the first successful run).

## Citation

```bibtex
@article{zhou2026wainf,
  title   = "WebArena-Infinity: Generating Browser Environments with Verifiable Tasks at Scale",
  author  = "Shuyan Zhou",
  journal = "shuyanzhou.com",
  year    = "2026",
  month   = "March",
  url     = "https://webarena.dev/webarena-infinity/"
}
```
