from pydantic import BaseModel, Field
from datetime import date
from typing import List

from constants import Gender


class ChapterGenerateRequestDto(BaseModel):
    gender: Gender = Field(default="FEMALE")
    occupation: str = Field(default="프로그래머")
    user_name: str = Field(default="최시원")
    date_of_birth: date = Field(
        default="2000-02-21"
    )  # ISO 형식의 날짜 (예: 1980-05-15)
    has_children: bool = Field(default=False)
    education_level: str = Field(default="대학교 재학")
    marital_status: str = Field(default="미혼")
    major_achievements: List[str] = Field(default_factory=list)  # 기본값 설정
    autobiography_theme: str = Field(default="인생사")  # 기본값 설정
