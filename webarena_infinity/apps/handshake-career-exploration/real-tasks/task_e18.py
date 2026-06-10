import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find question qa_12, then find answer ans_14 by Nathan Brooks
    qa_questions = state.get("qaQuestions", [])
    qa_12 = None
    for question in qa_questions:
        if question.get("id") == "qa_12":
            qa_12 = question
            break

    if qa_12 is None:
        return False, "Question qa_12 not found in qaQuestions."

    answers = qa_12.get("answers", [])
    ans_14 = None
    for answer in answers:
        if answer.get("id") == "ans_14":
            ans_14 = answer
            break

    if ans_14 is None:
        return False, f"Answer ans_14 not found in question qa_12. Available answers: {[a.get('id') for a in answers]}"

    helpful = ans_14.get("helpful", 0)
    if helpful <= 45:
        return False, f"Answer ans_14 helpful count is {helpful}, expected > 45."

    return True, f"Successfully marked Nathan Brooks's answer as helpful. helpful={helpful} > 45."
