import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from promptflow.core import Flow

from autobiographies.generate_autobiography.dto.request import (
    AutobiographyGenerateRequestDto,
)
from autobiographies.generate_autobiography.dto.response import (
    AutobiographyGenerateResponseDto,
)

router = APIRouter()


@router.post(
    "/api/v1/autobiographies/generate",
    response_model=AutobiographyGenerateResponseDto,
    tags=["자서전 (Autobiography)"],
)
def generate_autobiography(request: AutobiographyGenerateRequestDto):
    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load(
            "../flows/autobiographies/standard/generate_autobiography/flow.dag.yaml"
        )

        # 스트리밍 제너레이터 함수 정의
        def stream_autobiography():
            for text in flow(
                user_info=request.user_info,
                chapter_info=request.chapter_info,
                sub_chapter_info=request.sub_chapter_info,
                interview_chat=request.interviews,
            ).get("autobiographical_text", []):
                yield text

        # StreamingResponse로 제너레이터 반환
        return StreamingResponse(stream_autobiography(), media_type="text/plain")

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse the autobiography generation result.",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
