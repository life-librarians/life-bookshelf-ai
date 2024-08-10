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

    try:
        # Collect the results as they are returned by the flow
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
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
