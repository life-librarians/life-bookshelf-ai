from pydantic import BaseModel, Field

class GeneratedQuestionResponse(BaseModel):
    title: str = Field(default="주제", description="질문의 주제")
    subtitle: str = Field(default="소주제", description="질문의 소주제")
    subtopic: str = Field(default="소주제의 소주제", description="소주제의 소주제 설명")
    response: str = Field(default="호응", description="사용자 답변에 대한 호응")
    question: str = Field(default="질문", description="생성된 인터뷰 질문")
    is_next: bool = Field(default=True, description="다음 질문 생성 여부")
    is_over: bool = Field(default=False, description="모든 시스템 종료 여부")