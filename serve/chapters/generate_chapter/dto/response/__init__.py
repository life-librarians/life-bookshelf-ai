from pydantic import BaseModel, Field
from typing import List


class KeyEventDto(BaseModel):
    event_title: str
    event_description: str


class ChapterDto(BaseModel):
    chapter_title: str
    description: str
    key_events: List[KeyEventDto] = Field(default_factory=list)


class ChapterGenerateResponseDto(BaseModel):
    chapter_timeline: List[ChapterDto] = Field(default_factory=list)
