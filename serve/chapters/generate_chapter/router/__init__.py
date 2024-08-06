from fastapi import HTTPException, APIRouter

from chapters.generate_chapter.dto.request import ChapterGenerateRequestDto
from chapters.generate_chapter.dto.response import (
    ChapterGenerateResponseDto,
    ChapterDto,
    KeyEventDto,
)

router = APIRouter()


@router.post(
    "/chapters/generate_chapters",
    response_model=ChapterGenerateResponseDto,
    tags=["챕터 (Chapter)"],
)
def generate_chapters(request: ChapterGenerateRequestDto):
    if request.name.strip() == "":
        raise HTTPException(
            status_code=400, detail="Name is required and cannot be empty."
        )

    # TODO: Implement the logic to generate chapters based on the user data
    chapters = [
        ChapterDto(
            chapter_title="유년기 (0-10세)",
            description=f"이 챕터는 {request.name}의 출생부터 10세까지의 시기를 다룹니다.",
            key_events=[
                KeyEventDto(
                    event_title="첫 기억",
                    event_description=f"{request.name}의 가장 오래된 추억이나 중요한 어린 시절 경험",
                ),
                KeyEventDto(
                    event_title="초등학교 입학",
                    event_description=f"{request.name}의 초등학교 입학과 그로 인한 변화",
                ),
            ],
        )
    ]
    response = ChapterGenerateResponseDto(chapter_timeline=chapters)
    return response
