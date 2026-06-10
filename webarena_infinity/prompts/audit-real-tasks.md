Audit the agent evaluation results following the guide at `./docs/real-task-audit.md.`

**Result directories to audit:**
{evaluation_result_path}

Examine each result directory above. Each contains per-task folders with history.json, result.json, and screenshots/. Focus on **failed** tasks to determine root cause.

**Always** write an audit summary to the most recent result directory's `audit_summary.md` documenting your findings. Include:
- Overall pass rate and task counts (across all result dirs)
- For each failed task: the root cause (verifier bug, impossible task, ambiguous instruction, or agent-side failure) and any fix applied
- A summary of agent-side failures by category (navigation failure, wrong value, false claim, timeout, etc.)