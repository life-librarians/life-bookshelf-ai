import json

from fastapi import APIRouter, HTTPException, Depends
from promptflow.core import Flow
from pydantic_core import ValidationError
from starlette.requests import Request

from auth import MemberRole, AuthRequired, get_current_user
from interviews.generate_interview_question.dto.request import (
    InterviewQuestionGenerateRequestDto,
)
from interviews.generate_interview_question.dto.response import (
    InterviewQuestionGenerateResponseDto,
)
from logs import get_logger

logger = get_logger()

router = APIRouter()


@router.post(
    "/api/v1/interviews/interview-questions",
    dependencies=[Depends(AuthRequired())],
    response_model=InterviewQuestionGenerateResponseDto,
    summary="인터뷰 질문 생성",
    description="유저의 정보와 챕터 정보를 입력받아 인터뷰 질문을 생성합니다.",
    tags=["인터뷰 (Interview)"],
)
async def generate_interview_questions(
    request: Request, requestDto: InterviewQuestionGenerateRequestDto
):
    current_user = get_current_user(request)
    if requestDto.user_info.user_name.strip() == "":
        raise HTTPException(
            status_code=400, detail="Name is required and cannot be empty."
        )

    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load(
            "../flows/interviews/standard/generate_inteview_questions/flow.dag.yaml"
        )
        chapters = flow(
            user_info=requestDto.user_info,
            chapter_info=requestDto.chapter_info,
            sub_chapter_info=requestDto.sub_chapter_info,
        )

        # Directly accumulate chapter content into the result string
        result = "".join(chapters.get("interview_questions", []))

        # Parse the accumulated result string into a dictionary
        parsed_result = json.loads(result)

        # Create and return the response DTO
        response = InterviewQuestionGenerateResponseDto(**parsed_result)
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
