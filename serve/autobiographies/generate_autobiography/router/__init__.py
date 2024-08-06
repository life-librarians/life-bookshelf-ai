from fastapi import APIRouter, HTTPException

from autobiographies.generate_autobiography.dto.request import (
    AutobiographyGenerateRequestDto,
)
from autobiographies.generate_autobiography.dto.response import (
    AutobiographyGenerateResponseDto,
)

router = APIRouter()


def generate_autobiographical_text(
    user_info, chapter_info, sub_chapter_info, interview_contents
):
    narrative = f"{chapter_info.title}, 중반, 나 {user_info.name}의 인생에 큰 전환점이 찾아왔다. "
    narrative += f"{sub_chapter_info.description}. "

    for interview in interview_contents:
        if interview.conversationType == "HUMAN":
            narrative += f"{interview.content} "

    narrative += "이러한 경험들은 나의 성장에 큰 영향을 끼쳤다."
    return narrative


@router.post(
    "/api/v1/autobiographies/generate",
    response_model=AutobiographyGenerateResponseDto,
    tags=["자서전 (Autobiography)"],
)
def generate_autobiography(request: AutobiographyGenerateRequestDto):
    user_info = request.user_info
    chapter_info = request.chapter_info
    sub_chapter_info = request.sub_chapter_info
    interview_contents = request.interview

    autobiographical_text = generate_autobiographical_text(
        user_info, chapter_info, sub_chapter_info, interview_contents
    )

    if not autobiographical_text:
        raise HTTPException(
            status_code=404, detail="Unable to generate autobiographical text"
        )

    return AutobiographyGenerateResponseDto(autobiographical_text=autobiographical_text)
