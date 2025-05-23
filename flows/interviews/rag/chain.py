from .retriever import get_retriever
from .prompt import qa_prompt
from .llm import get_llm
from .memory import get_session_history

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from operator import itemgetter

def build_rag_chain():
    retriever = get_retriever()
    llm = get_llm()

    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
