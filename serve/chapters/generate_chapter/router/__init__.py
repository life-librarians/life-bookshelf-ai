import json

from fastapi import HTTPException, APIRouter, Depends
from promptflow.core import Flow
from pydantic_core import ValidationError
from starlette.requests import Request

from auth import MemberRole, get_current_user, AuthRequired
from chapters.generate_chapter.dto.request import ChapterGenerateRequestDto
from chapters.generate_chapter.dto.response import (
    ChapterGenerateResponseDto,
)
from logs import get_logger

logger = get_logger()

router = APIRouter()


@router.post(
    "/api/v1/chapters/generate_chapters",
    dependencies=[Depends(AuthRequired())],
    response_model=ChapterGenerateResponseDto,
    summary="자서전 챕터 생성",
    description="유저의 정보와 주제를 입력받아 자서전 챕터 정보를 생성합니다.",
    tags=["챕터 (Chapter)"],
)
async def generate_chapters(request: Request, requestDto: ChapterGenerateRequestDto):
    current_user = get_current_user(request)
    logger.info(f"Current user: {current_user}")
    if requestDto.user_name.strip() == "":
        raise HTTPException(
            status_code=400, detail="Name is required and cannot be empty."
        )

    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load("../flows/chapters/standard/generate_chapter/flow.dag.yaml")
        chapters = flow(
            gender=requestDto.gender,
            occupation=requestDto.occupation,
            user_name=requestDto.user_name,
            date_of_birth=requestDto.date_of_birth,
            has_children=requestDto.has_children,
            education_level=requestDto.education_level,
            marital_status=requestDto.marital_status,
            major_achievements=requestDto.major_achievements,
            autobiography_theme=requestDto.autobiography_theme,
        )

        # Directly accumulate chapter content into the result string
        result = "".join(chapters.get("chapter_timeline", []))

        # Parse the accumulated result string into a dictionary
        parsed_result = json.loads(result)

        # Create and return the response DTO
        response = ChapterGenerateResponseDto(**parsed_result)
        return response

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse the chapter generation result."
        )

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
