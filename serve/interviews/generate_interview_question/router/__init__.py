import json
from typing import List

from fastapi import APIRouter, HTTPException
from promptflow.core import Flow

from interviews.generate_interview_question.dto.request import (
    InterviewQuestionGenerateRequestDto,
)
from interviews.generate_interview_question.dto.response import (
    InterviewQuestionGenerateResponseDto,
)

router = APIRouter()


@router.post(
    "/api/v1/interviews/interview-questions",
    response_model=InterviewQuestionGenerateResponseDto,
    tags=["인터뷰 (Interview)"],
)
def generate_interview_questions(request: InterviewQuestionGenerateRequestDto):
    if request.user_info.user_name.strip() == "":
        raise HTTPException(
            status_code=400, detail="Name is required and cannot be empty."
        )

    try:
        # Collect the results as they are returned by the flow
        flow = Flow.load(
            "../flows/interviews/standard/generate_inteview_questions/flow.dag.yaml"
        )
        chapters = flow(
            user_info=request.user_info,
            chapter_info=request.chapter_info,
            sub_chapter_info=request.sub_chapter_info,
        )

        # Directly accumulate chapter content into the result string
        result = "".join(chapters.get("interview_questions", []))

        # Parse the accumulated result string into a dictionary
        parsed_result = json.loads(result)

        # Create and return the response DTO
        response = InterviewQuestionGenerateResponseDto(**parsed_result)
        return response
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse the chapter generation result."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
