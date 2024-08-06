from pydantic import BaseModel
from datetime import date

from constants import Gender


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


class InterviewQuestionGenerateRequestDto(BaseModel):
    user_info: UserInfoDto
    chapter_info: ChapterInfoDto
    sub_chapter_info: SubChapterInfoDto
