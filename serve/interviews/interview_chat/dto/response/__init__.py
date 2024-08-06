from typing import List

from pydantic import BaseModel, Field

from constants import ConversationType


class InterviewContentDto(BaseModel):
    content: str
    conversationType: ConversationType


class InterviewChatResponseDto(BaseModel):
    conversations: List[InterviewContentDto]
    bot_question: str
