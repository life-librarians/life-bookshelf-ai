from pydantic import BaseModel, Field
from datetime import date
from typing import List


class ChapterGenerateRequestDto(BaseModel):
    name: str
    date_of_birth: date  # ISO 형식의 날짜 (예: 1980-05-15)
    gender: str
    has_children: bool
    occupation: str
    education_level: str
    marital_status: str
    major_achievements: List[str] = Field(default_factory=list)  # 기본값 설정
    autobiography_theme: str = "User's Life"  # 기본값 설정
