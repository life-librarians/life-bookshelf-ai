import os
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
import pandas as pd

prompt = PromptTemplate.from_template(
    """당신은 사용자의 자서전을 돕는 인터뷰 질문 생성 AI입니다.

다음은 사용자의 최근 답변입니다:
"{answer}"

관련 참고 문서 (RAG 검색 결과):
{context}

위의 정보를 바탕으로, 자서전을 더욱 풍부하게 만들 수 있는 **다음 인터뷰 질문 하나를 생성**해주세요.

**질문은 반드시 아래 조건을 만족해야 합니다:**
- 사용자의 이전 답변과 중복되지 않은 **새로운 질문**일 것
- 사용자가 **감정**, **동기**, **배경**, **맥락** 등을 자연스럽게 회상하게 도와줄 것
- 마치 **지금 대화를 이어가는 흐름처럼 자연스럽게 연결**될 것

응답은 아래와 같은 **JSON 형식으로** 출력해주세요:

```json
{{
  "question": "생성된 인터뷰 질문",
  "is_next": true,
  "is_over": false
}}
"""
)