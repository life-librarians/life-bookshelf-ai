from typing import List

from fastapi import APIRouter, HTTPException

from interviews.interview_chat.dto.response import InterviewChatResponseDto

router = APIRouter()


@router.post(
    "/api/v1/interviews/interview-chat",
    response_model=InterviewChatResponseDto,
    summary="인터뷰 대화 생성",
    description="대화 히스토리를 토대로 다음 질문을 생성합니다.",
    tags=["인터뷰 (Interview)"],
)
def generate_interview_chat():
    # Simulate generating interview chat responses
    conversations = [
        {
            "content": "안녕하세요! 반가워요. 저는 인터뷰 봇입니다.",
            "conversationType": "BOT",
        },
        {
            "content": "안녕하세요! 반가워요. 저는 인터뷰 봇입니다.",
            "conversationType": "USER",
        },
    ]
    bot_question = "어떤 주제로 인터뷰를 진행하고 싶으신가요?"
    return InterviewChatResponseDto(
        conversations=conversations, bot_question=bot_question
    )
