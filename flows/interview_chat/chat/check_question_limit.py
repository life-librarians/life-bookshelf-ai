from promptflow.core import tool

@tool
def check_question_limit(chat_history: list, limit: int) -> str:
    if len(chat_history) >= limit:
        return "[STOP]"
    else:
        return "[CONTINUE]"
