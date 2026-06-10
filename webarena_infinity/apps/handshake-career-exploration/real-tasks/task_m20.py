import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    questions = state.get("qaQuestions", [])
    qa_06 = next((q for q in questions if q.get("id") == "qa_06"), None)
    if qa_06 is None:
        return False, "Q&A question qa_06 not found in state."

    answers = qa_06.get("answers", [])
    # Seed data has 1 answer (ans_09 by Kevin O'Brien). Look for a new semi-anonymous answer containing "mock".
    for answer in answers:
        if answer.get("id") == "ans_09":
            continue  # skip the existing seed answer
        visibility = answer.get("visibility", "")
        text = answer.get("text", "").lower()
        if visibility == "semi-anonymous" and "mock" in text:
            return True, (
                f"Found new semi-anonymous answer containing 'mock': '{answer.get('text')}'"
            )

    # Check what we do have for diagnostics
    new_answers = [a for a in answers if a.get("id") != "ans_09"]
    if not new_answers:
        return False, (
            f"No new answers found on qa_06. Only the seed answer (ans_09) exists."
        )

    return False, (
        f"New answers found on qa_06 but none match criteria "
        f"(visibility='semi-anonymous' and text containing 'mock'). "
        f"New answers: {[{'visibility': a.get('visibility'), 'text': a.get('text', '')[:80]} for a in new_answers]}"
    )
