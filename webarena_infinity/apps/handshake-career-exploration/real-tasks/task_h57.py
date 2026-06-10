"""
Task: Find the student who wrote about choosing a startup over Big Tech in the feed.
They also answered a Q&A question. Submit your own answer to that same question
sharing your perspective.

Discovery: Jordan Taylor wrote post_12 about startup vs Big Tech.
He authored ans_07 on qa_05 (salary negotiation).
Agent must submit a new answer to qa_05.

Verify: qa_05.answers has more than 2 entries (seed has ans_07 and ans_08).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()

    qa_questions = state.get("qaQuestions", [])
    qa_05 = next((q for q in qa_questions if q.get("id") == "qa_05"), None)
    if qa_05 is None:
        return False, "Question qa_05 (salary negotiation) not found."

    answers = qa_05.get("answers", [])
    if len(answers) <= 2:
        return False, (
            f"qa_05 has {len(answers)} answers, expected > 2 (seed has 2). "
            f"No new answer was submitted."
        )

    return True, (
        f"New answer submitted to qa_05 (salary negotiation). "
        f"Total answers: {len(answers)} (seed had 2)."
    )
