from pydantic import BaseModel, Field
from typing import List

class QuestionDto(BaseModel):
    question: str

class SubchapterDto(BaseModel):
    subchapter_title: str
    description: str
    questions: List[QuestionDto] = Field(default_factory=list)

class ChapterDto(BaseModel):
    chapter_title: str
    description: str
    subchapters: List[SubchapterDto] = Field(default_factory=list)

class ChapterGenerateResponseDto(BaseModel):
    chapter_timeline: List[ChapterDto] = Field(default_factory=list)