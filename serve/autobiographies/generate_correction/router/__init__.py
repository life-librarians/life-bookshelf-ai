import json
from typing import List

from fastapi import HTTPException, APIRouter, Depends
from promptflow.core import Flow
from starlette.requests import Request
from pydantic_core import ValidationError

from auth import AuthRequired, get_current_user
from autobiographies.generate_correction.dto.request import ProofreadingRequestDto
from autobiographies.generate_correction.dto.response import (
    CorrectionDto,
    ProofreadingResponseDto,
)
from logs import get_logger

logger = get_logger()

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
    dependencies=[Depends(AuthRequired())],
    response_model=ProofreadingResponseDto,
    tags=["자서전 (Autobiography)"],
    summary="자서전 교정/교열",
    description="자서전 내용을 교정하고 교열합니다. 교정 전 후 비교 결과를 배열에 담아 반환합니다.",
)
async def proofread_autobiography(request: Request, requestDto: ProofreadingRequestDto):
    current_user = get_current_user(request)
    logger.info(f"Proofreading autobiography for user {current_user.member_id}")

    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load(
            "../flows/autobiographies/standard/generate_correction/flow.dag.yaml"
        )
        corrections = flow(
            modified_text=requestDto.modified_text,
        )

        # Directly accumulate chapter content into the result string
        result = "".join(corrections.get("corrections", []))

        # Parse the accumulated result string into a dictionary
        parsed_result = json.loads(result)
        logger.info(parsed_result)

        # Create and return the response DTO
        response = ProofreadingResponseDto(**parsed_result)
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
