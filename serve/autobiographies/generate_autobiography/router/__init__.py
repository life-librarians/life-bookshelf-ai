import json

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from promptflow.core import Flow
from pydantic_core import ValidationError
from starlette.requests import Request

from auth import MemberRole, get_current_user, AuthRequired
from autobiographies.generate_autobiography.dto.request import (
    AutobiographyGenerateRequestDto,
)
from autobiographies.generate_autobiography.dto.response import (
    AutobiographyGenerateResponseDto,
)
from logs import get_logger

logger = get_logger()

router = APIRouter()


@router.post(
    "/api/v1/autobiographies/generate",
    dependencies=[Depends(AuthRequired())],
    response_model=AutobiographyGenerateResponseDto,
    summary="자서전 생성",
    description="유저의 정보와 챕터 정보, 인터뷰 대화 내역을 입력받아 자서전을 생성합니다.",
    tags=["자서전 (Autobiography)"],
)
async def generate_autobiography(
    request: Request,
    requestDto: AutobiographyGenerateRequestDto,
):
    current_user = get_current_user(request)
    try:
        logger.info(f"Generating autobiography for user {current_user.member_id}")
        # Collect the results as they are returned by the flow
        flow = Flow.load(
            "../flows/autobiographies/standard/generate_autobiography/flow.dag.yaml"
        )

        # 스트리밍 제너레이터 함수 정의
        def stream_autobiography():
            for text in flow(
                user_info=requestDto.user_info,
                chapter_info=requestDto.chapter_info,
                sub_chapter_info=requestDto.sub_chapter_info,
                interview_chat=requestDto.interviews,
            ).get("autobiographical_text", []):
                yield text

        # StreamingResponse로 제너레이터 반환
        return StreamingResponse(stream_autobiography(), media_type="text/plain")

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse the autobiography generation result.",
        )

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
