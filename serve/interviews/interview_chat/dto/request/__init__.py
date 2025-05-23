from pydantic import BaseModel, Field

class UserAnswerDto(BaseModel):
    answer: str = Field(default="20대")
    is_next: bool = Field(default=False)