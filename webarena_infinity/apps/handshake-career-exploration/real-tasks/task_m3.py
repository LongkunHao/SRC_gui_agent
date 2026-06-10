import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    current_user = state.get("currentUser", {})
    user_name = current_user.get("fullName", "")
    user_id = current_user.get("id", "")

    qa_questions = state.get("qaQuestions", [])

    for q in qa_questions:
        author_name = q.get("authorName", "")
        if author_name != user_name:
            continue

        question_text = q.get("question", "").lower()
        if "product management" in question_text and "interview" in question_text:
            return True, f"Found Q&A question by {author_name} about product management interviews."

    return False, "No Q&A question by Maya Chen found containing both 'product management' and 'interview'."
