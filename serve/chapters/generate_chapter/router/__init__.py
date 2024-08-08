import json

from fastapi import HTTPException, APIRouter
from promptflow.core import Flow

from chapters.generate_chapter.dto.request import ChapterGenerateRequestDto
from chapters.generate_chapter.dto.response import (
    ChapterGenerateResponseDto,
)

router = APIRouter()


@router.post(
    "/api/v1/chapters/generate_chapters",
    response_model=ChapterGenerateResponseDto,
    tags=["챕터 (Chapter)"],
)
def generate_chapters(request: ChapterGenerateRequestDto):
    if request.user_name.strip() == "":
        raise HTTPException(
            status_code=400, detail="Name is required and cannot be empty."
        )

    flow = Flow.load("../flows/chapters/standard/generate_chapter/flow.dag.yaml")
    chapters = flow(
        gender=request.gender,
        occupation=request.occupation,
        user_name=request.user_name,
        date_of_birth=request.date_of_birth,
        has_children=request.has_children,
        education_level=request.education_level,
        marital_status=request.marital_status,
        major_achievements=request.major_achievements,
        autobiography_theme=request.autobiography_theme,
    )

    result = ""
    for chapter in chapters.get("chapter_timeline"):
        result += chapter

    # JSON 문자열을 객체로 변환
    parsed_result = json.loads(result)

    # ChapterGenerateResponseDto 객체 생성
    response = ChapterGenerateResponseDto(**parsed_result)
    return response
