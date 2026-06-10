import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    questions = state.get("qaQuestions", [])
    qa_04 = next((q for q in questions if q.get("id") == "qa_04"), None)
    if qa_04 is None:
        return False, "Q&A question qa_04 not found in state."

    answers = qa_04.get("answers", [])
    # Seed data has 1 answer (ans_06). Check for a new answer containing "business casual".
    for answer in answers:
        if answer.get("id") == "ans_06":
            continue  # skip the existing seed answer
        text = answer.get("text", "").lower()
        if "business casual" in text:
            return True, f"Found new answer containing 'business casual': '{answer.get('text')}'"

    return False, (
        f"No new answer containing 'business casual' found on qa_04. "
        f"Current answers: {[a.get('text', '')[:80] for a in answers]}"
    )
