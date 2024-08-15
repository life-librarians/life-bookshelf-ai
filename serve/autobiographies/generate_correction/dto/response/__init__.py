from pydantic import BaseModel, Field
from typing import List


class CorrectionDto(BaseModel):
    original: str = Field(default="나는 20살때 처음으로 해외여행을 갔다.")
    corrected: str = Field(default="나는 20살 때 처음으로 해외여행을 갔다.")
    explanation: str = Field(default="'살'과 '때'는 띄어쓰기를 해야 합니다.")


class ProofreadingResponseDto(BaseModel):
    corrections: List[CorrectionDto] = Field(
        default=[
            CorrectionDto(),
            CorrectionDto(
                original="그것은 일본이였다.",
                corrected="그곳은 일본이었다.",
                explanation="'그것'보다는 '그곳'이 더 자연스럽고, '이였다'는 '이었다'로 써야 합니다.",
            ),
            CorrectionDto(
                original="귀국후 바로 학업에 열중해야 했기 때문에,",
                corrected="귀국 후 바로 학업에 열중해야 했기 때문에,",
                explanation="'귀국'과 '후'는 띄어쓰기를 해야 합니다.",
            ),
        ]
    )
