import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    questions = state.get("qaQuestions", [])
    errors = []

    # Check 1: qa_10 (finance internship recruiting timelines) has a new answer containing "network"
    qa_10 = next((q for q in questions if q.get("id") == "qa_10"), None)
    if qa_10 is None:
        errors.append("Q&A question qa_10 not found in state.")
    else:
        answers = qa_10.get("answers", [])
        found_answer = False
        for answer in answers:
            text = answer.get("text", "").lower()
            if "network" in text:
                found_answer = True
                break
        if not found_answer:
            errors.append(
                f"No answer containing 'network' found on qa_10. "
                f"Current answers: {[a.get('text', '')[:80] for a in answers]}"
            )

    # Check 2: In qa_05 (salary negotiation), ans_07 has helpful > 89
    qa_05 = next((q for q in questions if q.get("id") == "qa_05"), None)
    if qa_05 is None:
        errors.append("Q&A question qa_05 not found in state.")
    else:
        answers_05 = qa_05.get("answers", [])
        ans_07 = next((a for a in answers_05 if a.get("id") == "ans_07"), None)
        if ans_07 is None:
            errors.append("Answer ans_07 not found in qa_05.")
        else:
            helpful = ans_07.get("helpful", 0)
            if helpful <= 89:
                errors.append(
                    f"ans_07 on qa_05 has helpful={helpful}, expected > 89. "
                    f"The helpful action may not have been performed."
                )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Answer containing 'network' found on qa_10, and ans_07 on qa_05 has helpful > 89."
    )
