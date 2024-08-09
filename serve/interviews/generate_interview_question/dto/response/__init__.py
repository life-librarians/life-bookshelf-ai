from typing import List

from pydantic import BaseModel, Field


class InterviewQuestionGenerateResponseDto(BaseModel):
    questions: List[str] = Field(default_factory=list)