import json

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from pydantic_core import ValidationError

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from flows.interviews.rag.chain import build_rag_chain

from auth import AuthRequired, get_current_user
from serve.interviews.interview_chat.dto.request import UserAnswerDto
from serve.interviews.interview_chat.dto.response import GeneratedQuestionResponse
from logs import get_logger

logger = get_logger()

router = APIRouter()
rag_with_history = build_rag_chain()


@router.post(
    "/api/v1/interviews/interview-chat/rag",
    dependencies=[Depends(AuthRequired())],
    response_model=str, # 반환 형식이 문자열임.
    summary="RAG 기반 인터뷰 질문 생성",
    description="벡터 검색과 대화 히스토리를 기반으로 질문을 생성합니다.",
    tags=["인터뷰 (Interview)"],
)
async def generate_interview_chat_rag(
    request: Request, requestDto: UserAnswerDto
):
    current_user = get_current_user(request)

    try:
        question_input = {"question": requestDto.current_answer}
        session_id = f"user-{current_user.id}"  # 또는 requestDto.session_id

        # LLM으로부터 단순 문자열 질문 반환
        generated_question = rag_with_history.invoke(
            question_input, config={"configurable": {"session_id": session_id}}
        )

        # 문자열을 응답 DTO에 매핑
        return GeneratedQuestionResponse(
            question=generated_question,
            is_next=True,
            is_over=False
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse the chapter generation result."
        )

    except ValidationError as e:
        logger.error(f"Validation error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
