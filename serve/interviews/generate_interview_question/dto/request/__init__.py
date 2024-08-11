from pydantic import BaseModel, Field
from datetime import date

from constants import Gender


class UserInfoDto(BaseModel):
    user_name: str = Field(default="최시원")
    date_of_birth: date = Field(default="2000-02-21")
    gender: Gender = Field(default=Gender.FEMALE)
    occupation: str = Field(default="프로그래머")
    education_level: str = Field(default="대학교 재학")
    marital_status: str = Field(default="미혼")


class ChapterInfoDto(BaseModel):
    title: str = Field(default="20대")
    description: str = Field(default="대학 생활과 첫 직장 경험")


class SubChapterInfoDto(BaseModel):
    title: str = Field(default="첫 직장 생활")
    description: str = Field(default="소프트웨어 회사에서의 첫 직장 경험과 적응 과정")


class InterviewQuestionGenerateRequestDto(BaseModel):
    user_info: UserInfoDto = Field(default_factory=UserInfoDto)
    chapter_info: ChapterInfoDto = Field(default_factory=ChapterInfoDto)
    sub_chapter_info: SubChapterInfoDto = Field(default_factory=SubChapterInfoDto)
