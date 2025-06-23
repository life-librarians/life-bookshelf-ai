import json
import csv
import traceback
import redis
import httpx

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from flows.interviews.rag.chain import build_next_question_chain, generate_sugestions_chain, detect_topic_subtopic
from flows.interviews.rag.memory import get_session_history

from auth import AuthRequired, get_current_user
from serve.interviews.interview_chat.dto.request import UserAnswerDto
from serve.autobiographies.generate_autobiography.router import run_autobiography_flow
from serve.api.interviews.interview_chat import save_qa_to_main_server, update_current_subtopic
from serve.api.autobiographies.generate_autobiography import save_autobiography
from serve.interviews.interview_chat.dto.response import GeneratedQuestionResponse
from logs import get_logger

logger = get_logger()

router = APIRouter()
rag_with_history = build_next_question_chain()

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)  # Redis 연결 필요 (예제)

# 진행 상태 관리
def load_progress(session_id):
    data = r.get(session_id)
    return json.loads(data) if data else None

def save_progress(session_id, progress):
    r.set(session_id, json.dumps(progress))
    
# 질의응답 포맷 바꾸기
def flatten_interview(chapters: dict, title: str, subtitle: str) -> list:
    interview = []
    subtopics = chapters.get(title, {}).get(subtitle, {})
    for subtopic, qna_list in subtopics.items():
        for qa in qna_list:
            interview.append({"content": qa["Q"], "conversationType": "BOT"})
            interview.append({"content": qa["A"], "conversationType": "HUMAN"})
    return interview

@router.get("/health-check")
async def health_check():
    return JSONResponse(content={"message": "OK"}, status_code=200)

@router.post("/api/v1/interviews/interview-chat/rag", dependencies=[Depends(AuthRequired())], response_model=GeneratedQuestionResponse)
async def generate_interview_chat_rag(request: Request, requestDto: UserAnswerDto):
    current_user = get_current_user(request)
    session_id = f"user-{current_user.member_id}"
    access_token = request.headers.get("Authorization").split(" ")[1]

    try:
        progress = load_progress(session_id)
        user_answer = requestDto.answer

        if requestDto.is_first or not progress:
            first_question = "안녕 반가워! 나는 너의 이야기를 듣고 싶어. 먼저, 너에 대해 조금 소개해줄래?"
            progress = {
                "current": {}, "chapters": {}, "last_question": first_question,
                "current_question_index": 0, "pending_subquestions": [],
                "subtopic_finished": False, "subtopic_subquestions": {}, "first_answer_received": False
            }
            save_progress(session_id, progress)
            return GeneratedQuestionResponse(title="", subtitle="", subtopic="", response="", question=first_question, is_next=True, is_over=False)

        chat_history = get_session_history(session_id)

        user_profile = {
            "age_group": current_user.age_group or "20대",
            "gender": current_user.gender or "여자",
            "education_level": current_user.education_level or "대학교 재학",
            "marital_status": current_user.marital_status or "미혼"
        }

        if not progress.get("first_answer_received"):
            title, subtitle, subtopic, subtopics = detect_topic_subtopic(user_answer, user_profile, chat_history)
            progress["current"] = {"title": title, "subtitle": subtitle, "subtopic": subtopic}
            progress["current_subtopics"] = subtopics
            progress.setdefault("subtopic_status", {})
            progress["first_answer_received"] = True
            # await update_current_subtopic(title, subtitle, subtopic, access_token)
        else:
            title = progress["current"].get("title")
            subtitle = progress["current"].get("subtitle")
            subtopic = progress["current"].get("subtopic")

        subtopic_key = f"{title}::{subtitle}::{subtopic}"
        sub_data = progress["subtopic_subquestions"].get(subtopic_key)
        context = ""

        if not sub_data:
            q_data = rag_with_history.invoke({
                "answer": user_answer, "gender": user_profile["gender"], "age_group": user_profile["age_group"],
                "education_level": user_profile["education_level"], "marital_status": user_profile["marital_status"],
                "title": title, "subtitle": subtitle, "subtopic": subtopic,
                "context": context, "chat_history": chat_history
            }, config={"configurable": {"session_id": session_id}})

            recommended_question = q_data.get("question")
            context = q_data.get("context", "")
            response, subquestions = generate_sugestions_chain(recommended_question, user_answer, context, user_profile)

            if not subquestions:
                subquestions = [recommended_question]
            elif len(subquestions) == 1:
                subquestions.append("조금 더 자세히 이야기해줄 수 있을까?")

            sub_data = {"response": response, "subquestions": subquestions, "q_index": 0}
        else:
            response = sub_data["response"]
            subquestions = sub_data["subquestions"]

        q_index = sub_data.get("q_index", 0)
        pending = subquestions[q_index:] if q_index < len(subquestions) else []

        if pending:
            next_q = pending[0]
            sub_data["q_index"] += 1
            pending = pending[1:]
        else:
            response, subquestions = generate_sugestions_chain(progress.get("last_question"), user_answer, context, user_profile)
            if subquestions:
                sub_data["subquestions"] = subquestions
                sub_data["q_index"] = 1
                next_q = subquestions[0]
                pending = subquestions[1:]
            else:
                response = "그 경험에 대해 더 들려줄 수 있을까?"
                next_q = "계속 이야기해줘. 기억나는 게 더 있을까?"
                pending = []

        progress["pending_subquestions"] = pending
        progress["subtopic_subquestions"][subtopic_key] = sub_data
        chapters = progress.get("chapters", {})
        chapters.setdefault(title, {}).setdefault(subtitle, {}).setdefault(subtopic, []).append({
            "Q": progress.get("last_question"), "A": user_answer
        })
        progress["chapters"] = chapters

        # await save_qa_to_main_server(progress.get("last_question"), user_answer, access_token)

        progress["current"] = {"title": title, "subtitle": subtitle, "subtopic": subtopic}
        progress["last_question"] = next_q
        progress["subtopic_subquestions"][subtopic_key] = sub_data
        save_progress(session_id, progress)

        return GeneratedQuestionResponse(title=title, subtitle=subtitle, subtopic=subtopic, response=response, question=next_q, is_next=True, is_over=False)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the chapter generation result.")
    except ValidationError as e:
        logger.error(f"Validation error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")