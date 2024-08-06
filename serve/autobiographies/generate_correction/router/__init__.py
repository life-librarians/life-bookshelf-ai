from typing import List

from fastapi import HTTPException, APIRouter

from autobiographies.generate_correction.dto.request import ProofreadingRequestDto
from autobiographies.generate_correction.dto.response import (
    CorrectionDto,
    ProofreadingResponseDto,
)

router = APIRouter()


# Dummy function to simulate proofreading
def proofread_content(content: str) -> List[CorrectionDto]:
    # This is a simple simulation. In reality, you would integrate with an actual AI proofreading service.
    corrections = [
        CorrectionDto(original="김도훈", corrected="도훈 김"),
        CorrectionDto(original="1985년 3월 15일", corrected="March 15, 1985"),
        CorrectionDto(original="과학자가 되는 꿈", corrected="과학자의 꿈"),
    ]
    return corrections


@router.post(
    "/api/v1/autobiographies/proofreading",
    response_model=ProofreadingResponseDto,
    tags=["자서전 (Autobiography)"],
)
def proofread_autobiography(request: ProofreadingRequestDto):
    # Call the proofreading function
    corrections = proofread_content(request.content)

    if not corrections:
        raise HTTPException(status_code=404, detail="No corrections found")

    response = ProofreadingResponseDto(corrections=corrections)
    return response
