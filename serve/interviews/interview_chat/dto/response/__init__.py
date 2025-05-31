from pydantic import BaseModel, Field

class GeneratedQuestionResponse(BaseModel):
    question: str = Field(..., description="생성된 인터뷰 질문")
    is_next: bool = Field(default=True, description="다음 질문 생성 여부")
    is_over: bool = Field(default=False, description="모든 시스템 종료 여부")