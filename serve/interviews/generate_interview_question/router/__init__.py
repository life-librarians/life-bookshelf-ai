from typing import List

from fastapi import APIRouter, HTTPException

from interviews.generate_interview_question.dto.request import (
    InterviewQuestionGenerateRequestDto,
)
from interviews.generate_interview_question.dto.response import (
    InterviewQuestionGenerateResponseDto,
)

router = APIRouter()


def generate_questions_based_on_input(
    request: InterviewQuestionGenerateRequestDto,
) -> List[str]:
    # Generate questions based on the autobiography details provided
    return [
        "What was the most challenging experience you faced during your childhood?",
        "Who was your role model growing up and why?",
        "What is the most important lesson you learned from your parents?",
    ]


@router.post(
    "/api/v1/interviews/interview-questions",
    response_model=InterviewQuestionGenerateResponseDto,
    tags=["인터뷰 (Interview)"],
)
def generate_interview_questions(request: InterviewQuestionGenerateRequestDto):
    # Simulate generating questions based on the autobiography details provided
    questions = generate_questions_based_on_input(request)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions generated")
    return InterviewQuestionGenerateResponseDto(questions=questions)
