from pydantic import BaseModel, Field

from constants import Gender


class ChapterGenerateRequestDto(BaseModel):
    gender: Gender = Field(default="FEMALE")
    age: str = Field(
        default="20대"
    )  
    education_level: str = Field(default="대학교 재학")
    marital_status: str = Field(default="미혼")
