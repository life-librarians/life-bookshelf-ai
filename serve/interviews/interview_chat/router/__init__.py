import json
import csv
import traceback
import redis
import httpx

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from pydantic_core import ValidationError

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from flows.interviews.rag.chain import build_next_question_chain, generate_sugestions_chain, detect_topic_subtopic
from flows.interviews.rag.memory import get_session_history

from auth import AuthRequired, get_current_user
from serve.interviews.interview_chat.dto.request import UserAnswerDto
from serve.api.interviews.interview_chat import save_qa_to_main_server, update_current_subtopic, trigger_autobiography_generation
from serve.interviews.interview_chat.dto.response import GeneratedQuestionResponse
from logs import get_logger

logger = get_logger()

router = APIRouter()
rag_with_history = build_next_question_chain()

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  # Redis 연결 필요 (예제)

# 진행 상태 관리
def load_progress(session_id):
    data = r.get(session_id)
    return json.loads(data) if data else None

def save_progress(session_id, progress):
    r.set(session_id, json.dumps(progress))

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
                "current": {},
                "chapters": {},
                "last_question": first_question,
                "current_question_index": 0,
                "pending_subquestions": [],
                "subtopic_finished": False,
                "subtopic_subquestions": {}
            }
            save_progress(session_id, progress)
            return GeneratedQuestionResponse(
                title="", subtitle="", subtopic="",
                response="알겠어!", question=first_question,
                is_next=True, is_over=False
            )

        chat_history = get_session_history(session_id)
        is_first_answer = not bool(progress.get("current", {}).get("title"))

        if is_first_answer or (not progress.get("pending_subquestions") and progress.get("subtopic_finished", False)):
            user_profile = {
                "age_group": current_user.age_group or "20대",
                "gender": current_user.gender or "여자",
                "education_level": current_user.education_level or "대학교 재학",
                "marital_status": current_user.marital_status or "미혼"
            }
            title, subtitle, subtopic = detect_topic_subtopic(user_answer, user_profile, chat_history)
            progress["current"] = {"title": title, "subtitle": subtitle, "subtopic": subtopic}
            progress["subtopic_finished"] = False
            
            # sub topic 감지 후 변경 요청
            await update_current_subtopic(
                title=title,
                subtitle=subtitle,
                subtopic=subtopic,
                access_token=access_token
            )

        else:
            title = progress["current"].get("title")
            subtitle = progress["current"].get("subtitle")
            subtopic = progress["current"].get("subtopic")

        subtopic_key = f"{title}::{subtitle}::{subtopic}"
        sub_data = progress["subtopic_subquestions"].get(subtopic_key)

        if not sub_data:
            # 질문 생성
            q_data = rag_with_history.invoke(
                {
                    "answer": user_answer,
                    "gender": current_user.gender,
                    "age_group": current_user.age_group,
                    "education_level": current_user.education_level,
                    "marital_status": current_user.marital_status,
                    "title": title,
                    "subtitle": subtitle,
                    "subtopic": subtopic,
                    "context": context,
                    "chat_history": chat_history,
                },
                config={"configurable": {"session_id": session_id}}
            )

            recommended_question = q_data.get("question")
            context = q_data.get("context", "")

            user_profile = {
                "age_group": current_user.age_group or "20대",
                "gender": current_user.gender or "여자",
                "education_level": current_user.education_level or "대학교 재학",
                "marital_status": current_user.marital_status or "미혼"
            }

            response, subquestions = generate_sugestions_chain(
                parent_question=recommended_question,
                user_answer=user_answer,
                context=context,
                user_profile=user_profile
            )

            sub_data = {
                "response": response,
                "subquestions": subquestions,
                "q_index": 0
            }
            progress["subtopic_subquestions"][subtopic_key] = sub_data
        else:
            response = sub_data["response"]
            subquestions = sub_data["subquestions"]

        pending = progress.get("pending_subquestions", [])
        if not pending and subquestions:
            next_q = subquestions[0]
            pending = subquestions[1:]
        else:
            next_q = pending[0] if pending else "더 궁금한 점이 있니?"
            pending = pending[1:] if pending else []

        progress["pending_subquestions"] = pending
        if not pending:
            progress["subtopic_finished"] = True

            # 모든 subtopic이 종료됐는지 검사
            all_subtopics = progress.get("chapters", {}).get(title, {}).get(subtitle, {})
            finished = True
            for sub_k in all_subtopics:
                key = f"{title}::{subtitle}::{sub_k}"
                if not progress["subtopic_subquestions"].get(key):
                    finished = False
                elif not progress["subtopic_finished"]:
                    finished = False

            if finished:
                await trigger_autobiography_generation(
                    title=title,
                    subtitle=subtitle,
                    chapters=all_subtopics,
                    access_token=access_token
                )

            # 자서전 트리거 후 진행 상태 초기화 or 마무리 멘트
            progress["last_question"] = "우리 제일 최근에 {}에 대해서 이야기했었지. 오늘은 무슨 얘기를 해볼까?".format(subtopic)
            save_progress(session_id, progress)

            return GeneratedQuestionResponse(
                title=title,
                subtitle=subtitle,
                subtopic=subtopic,
                response="오늘의 이야기는 끝이야 ! 우리 내일 다시 만나자 !",
                question=progress["last_question"],
                is_next=True,
                is_over=True 
            )

        progress["current"] = {"title": title, "subtitle": subtitle, "subtopic": subtopic}
        chapters = progress.get("chapters", {})
        chapters.setdefault(title, {}).setdefault(subtitle, {}).setdefault(subtopic, [])
        chapters[title][subtitle][subtopic].append({
            "Q": progress.get("last_question"),
            "A": user_answer
        })
        
        # 질문 답변 저장 요청
        await save_qa_to_main_server(
            title=title,
            subtitle=subtitle,
            subtopic=subtopic,
            question=progress.get("last_question"),
            answer=user_answer,
            access_token=access_token
        )
        
        progress["chapters"] = chapters
        progress["last_question"] = next_q
        save_progress(session_id, progress)

        return GeneratedQuestionResponse(
            title=title, subtitle=subtitle, subtopic=subtopic,
            response=response, question=next_q,
            is_next=True, is_over=False
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the chapter generation result.")
    except ValidationError as e:
        logger.error(f"Validation error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")