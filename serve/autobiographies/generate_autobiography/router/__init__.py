from promptflow.core import Flow

from auth import MemberRole, get_current_user, AuthRequired
from autobiographies.generate_autobiography.dto.request import (
    AutobiographyGenerateRequestDto,
)
from autobiographies.generate_autobiography.dto.response import (
    AutobiographyGenerateResponseDto,
)
from logs import get_logger
from fastapi import APIRouter

router = APIRouter()

logger = get_logger()

async def run_autobiography_flow(
    user_info: dict,
    chapter_info: dict,
    sub_chapter_info: list,
    interviews: list
) -> str:
    flow = Flow.load("../flows/autobiographies/standard/generate_autobiography/flow.dag.yaml")

    result = flow(
        user_info=user_info,
        chapter_info=chapter_info,
        sub_chapter_info=sub_chapter_info,
        interview_chat=interviews,
    )

    return result.get("autobiographical_text")