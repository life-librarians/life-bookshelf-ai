from datetime import date
from typing import List
from pydantic import BaseModel, Field

from constants import Gender, ConversationType


class UserInfoDto(BaseModel):
    name: str = Field(default="최시원")
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


class InterviewContentDto(BaseModel):
    content: str = Field(
        default="회사에서 맡은 첫 프로젝트는 무엇이었고, 어떤 도전이 있었나요?"
    )
    conversation_type: ConversationType = Field(default=ConversationType.BOT)


class AutobiographyGenerateRequestDto(BaseModel):
    user_info: UserInfoDto
    chapter_info: ChapterInfoDto
    sub_chapter_info: SubChapterInfoDto
    interviews: List[InterviewContentDto] = Field(
        default=[
            InterviewContentDto(),
            InterviewContentDto(
                content="제가 맡은 첫 프로젝트는 온라인 쇼핑몰 구축 프로젝트였습니다. 처음으로 프로젝트를 맡아서 설계부터 개발까지 전반적인 업무를 담당했는데, 기존에 경험이 부족했기 때문에 많은 어려움을 겪었습니다. 특히, 프로젝트 일정이 타이트했기 때문에 개발 과정에서 많은 야근을 했었죠.",
                conversationType=ConversationType.HUMAN,
            ),
        ]
    )
