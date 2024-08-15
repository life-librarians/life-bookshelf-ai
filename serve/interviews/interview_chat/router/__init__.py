import json
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from promptflow.core import Flow
from starlette.requests import Request
from pydantic_core import ValidationError

from auth import AuthRequired, get_current_user
from interviews.interview_chat.dto.request import InterviewChatRequestDto
from interviews.interview_chat.dto.response import InterviewChatResponseDto
from logs import get_logger

logger = get_logger()

router = APIRouter()


@router.post(
    "/api/v1/interviews/interview-chat",
    dependencies=[Depends(AuthRequired())],
    response_model=InterviewChatResponseDto,
    summary="인터뷰 대화 생성",
    description="대화 히스토리를 토대로 다음 질문을 생성합니다.",
    tags=["인터뷰 (Interview)"],
)
async def generate_interview_chat(
    request: Request, requestDto: InterviewChatRequestDto
):
    current_user = get_current_user(request)

    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load("../flows/interviews/standard/interview_chat/flow.dag.yaml")
        chapters = flow(
            user_info=requestDto.user_info,
            chapter_info=requestDto.chapter_info,
            sub_chapter_info=requestDto.sub_chapter_info,
            conversation_history=requestDto.conversation_history,
            current_answer=requestDto.current_answer,
            question_limit=requestDto.question_limit,
        )

        # Directly accumulate chapter content into the result string
        result = "".join(chapters.get("interview_questions", []))

        # Parse the accumulated result string into a dictionary
        parsed_result = json.loads(result)

        # Create and return the response DTO
        response = InterviewChatResponseDto(**parsed_result)
        return response
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
