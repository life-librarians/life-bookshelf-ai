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
    has_children: bool
    chosen_theme: str


class InterviewChatRequestDto(BaseModel):
    user_info: UserInfoDto
    user_answer: str
