from flows.interviews.data.load_and_split import ensure_split_documents

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from operator import itemgetter

import json
import re
import os

# 초기화 시 split_documents.pkl 생성
ensure_split_documents()

from .retriever import get_retriever
from .prompt import initial_prompt, followup_prompt, subquestion_prompt
from .llm import get_llm
from .memory import get_session_history

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'topics.json')

# JSON 파일 로드
with open(file_path, 'r', encoding='utf-8') as f:
    questions_meta = json.load(f)
        
# 다음 질문 추천 generation
def build_next_question_chain():
    retriever = get_retriever()
    llm = get_llm()

    # LangChain 최신 방식: LLMChain 대신 prompt | llm
    followup_chain = followup_prompt | llm

    # 전체 체인 구성 (RunnableSequence 사용)
    chain = (
        {
            "answer": itemgetter("answer"),
            "context": itemgetter("context") | retriever,
            "chat_history": itemgetter("chat_history"),
            "title": itemgetter("title"),  # 추가
            "subtitle": itemgetter("subtitle"),  # 추가
            "subtopic": itemgetter("subtopic"),
            "age_group": itemgetter("age_group"),
            "gender": itemgetter("gender"),
            "education_level": itemgetter("education_level"),
            "marital_status": itemgetter("marital_status"),
        }
        | followup_chain
        | JsonOutputParser() # JSON 파싱을 위한 출력 파서
    )
    
    print("build_next_question_chain:", chain)

    # Message History 포함
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="answer",
        history_messages_key="chat_history",
    )

# sub topic 매핑 generation
def generate_sugestions_chain(parent_question, user_answer, context, user_profile):
    
    llm = get_llm()
    subquestion_prompt_llm_chain = subquestion_prompt | llm
    
    # input은 하나의 dict로 묶어서 넘겨야 합니다.
    input_data = {
        "parent_question": parent_question,
        "answer": user_answer,
        "context": context,
        "age_group": user_profile["age_group"],
        "gender": user_profile["gender"],
        "education_level": user_profile["education_level"],
        "marital_status": user_profile["marital_status"]
    }

    result = subquestion_prompt_llm_chain.invoke(input_data)
    
    json_str = re.sub(r'^```json\n|\n```$', '', result.content.strip())
    
    print("generate_sugestions_chain result:", json_str)
    
    parsed = json.loads(json_str)
    response = parsed.get("response", "좋아!")
    subquestions = parsed.get("subquestions", [])
    return response, subquestions

# 주제 및 하위 주제 감지
def detect_topic_subtopic(user_answer, user_profile, chat_history):
    llm = get_llm()
    
    prompt_input = {
        "answer": user_answer,
        "questions_meta": questions_meta,
        "chat_history": chat_history,
        "age_group": user_profile.get("age_group", "20대"),
        "gender": user_profile.get("gender", "여자"),
        "education_level": user_profile.get("education_level", "대학교 재학"),
        "marital_status": user_profile.get("marital_status", "미혼"),
        }

    intial_llm_chain = initial_prompt | llm
    
    result = intial_llm_chain.invoke(prompt_input)
    json_str = re.sub(r'^```json\n|\n```$', '', result.content.strip())
    
    print("detect_topic_subtopic result:", json_str)
    
    parsed = json.loads(json_str)
    
    # 주제 및 하위 주제 추출
    return (
        parsed.get("title"),
        parsed.get("subtitle"),
        parsed.get("subtopic"),
        parsed.get("subtopics", [parsed.get("subtopic")])  # 전체 목록, 없으면 단일 subtopic 하나라도 반환
    )
