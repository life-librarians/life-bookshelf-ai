from datetime import date
from typing import List
from pydantic import BaseModel, Field

from constants import Gender, ConversationType


class UserInfoDto(BaseModel):
    name: str
    date_of_birth: date
    gender: Gender
    occupation: str
    education_level: str
    marital_status: str


class ChapterInfoDto(BaseModel):
    title: str
    description: str


class SubChapterInfoDto(BaseModel):
    title: str
    description: str


class InterviewContentDto(BaseModel):
    content: str
    conversationType: ConversationType


class AutobiographyGenerateRequestDto(BaseModel):
    user_info: UserInfoDto
    chapter_info: ChapterInfoDto
    sub_chapter_info: SubChapterInfoDto
    interview: List[InterviewContentDto] = Field(default_factory=list)
