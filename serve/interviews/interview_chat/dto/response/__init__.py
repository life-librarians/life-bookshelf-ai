from typing import List
from pydantic import BaseModel, Field


class InterviewChatResponseDto(BaseModel):
    interview_questions: List[str] = Field(default_factory=list)
