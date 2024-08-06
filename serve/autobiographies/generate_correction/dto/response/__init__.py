from pydantic import BaseModel, Field
from typing import List


class CorrectionDto(BaseModel):
    original: str
    corrected: str


class ProofreadingResponseDto(BaseModel):
    corrections: List[CorrectionDto] = Field(default_factory=list)
