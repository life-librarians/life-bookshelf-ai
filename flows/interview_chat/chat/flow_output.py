from promptflow.core import tool

@tool
def flow_output(stop_or_continue: str, question: str) -> str:
    if stop_or_continue == '[STOP]':
        return "[STOP]"
    else:
        return question
