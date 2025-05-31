from flows.interviews.data.load_and_split import ensure_split_documents

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from operator import itemgetter

# 초기화 시 split_documents.pkl 생성
ensure_split_documents()

from .retriever import get_retriever
from .prompt import initial_prompt, followup_prompt
from .llm import get_llm
from .memory import get_session_history

def build_rag_chain():
    retriever = get_retriever()
    llm = get_llm()

    # LangChain 최신 방식: LLMChain 대신 prompt | llm
    initial_chain = initial_prompt | llm
    followup_chain = followup_prompt | llm

    # 라우팅 함수: is_first에 따라 initial 또는 chapter 체인 선택
    def router_func(inputs):
        if inputs.get("is_first", True):
            return initial_chain
        else:
            return followup_chain

    router_runnable = RunnableLambda(router_func)

    # 전체 체인 구성 (RunnableSequence 사용)
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
            "is_first": itemgetter("is_first"),
        }
        | router_runnable
        | StrOutputParser()
    )

    # Message History 포함
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
