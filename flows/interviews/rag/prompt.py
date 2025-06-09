import os
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
import pandas as pd

initial_prompt = PromptTemplate.from_template("""
당신은 사용자의 자서전을 돕는 AI입니다.
사용자가 첫 대답을 주면, 해당 대답을 기반으로 적합한 '주제'와 '소주제'를 선택하고, 선택한 소주제에 맞춘 컨셉의 '소주제의 소주제(subtopic)'까지 생성하세요.

사용자가 말한 첫 대답:
"{answer}"

사용자의 이전 session 정보 및 배경 지식:
{chat_history}

사용자의 정보는 다음과 같습니다:
- 연령대: {age_group}
- 성별: {gender}
- 학력: {education_level}
- 결혼 여부: {marital_status}


- 사용자 답변의 의미를 분석하여 가장 적합한 주제(title)와 소주제(subtitle)를 선택
- 반드시 위 리스트에 포함된 title/subtitle만 선택
- subtitle 선택 후, 해당 소주제를 구체적으로 설명하는 subtopic도 작성

응답은 아래 JSON 형식으로 출력:
```json
{{
  "title": "{{title}}",
  "subtitle": "{{subtitle}}",
  "subtopic": "{{subtopic}}",
  "reason": "선택 이유"
}}
"""
)

followup_prompt = PromptTemplate.from_template(
    """
당신은 사용자의 자서전을 돕는 인터뷰 질문 생성 AI입니다.

다음은 사용자의 최근 답변입니다:
"{answer}"

관련 참고 문서 :
{chat_history}

사용자가 이전에 이야기한 주제(title)와 subtitle은 유지하며, 다음 질문을 생성할 때,
- 만약 사용자가 해당 주제(subtitle)에 대한 이야기를 충분히 한 것 같다면, 다음 주제로 넘어갈지 물어보는 질문을 생성하세요.
- 만약 사용자가 더 이야기할 여지가 있다면, 해당 주제의 다음 질문을 생성하세요.

다음은 선택 가능한 title/subtitle 리스트입니다:
- 성장과정: 출생, 첫 독립, 첫 실패, 부모와의 거리감
- 가족관계: 부모, 형제자매, 자녀, 조부모, 반려동물, 배우자
- 학창시절: 학교 생활, 친구 관계, 과목 수업, 동아리 활동
- 직업/진로: 진로 선택 계기, 업무 에피소드, 대외활동, 번아웃 경험
- 가치관/성격: 성격 변화, 신념 형성 계기, 철학적 사고, 인생의 전환점
- 인생 경험: 어려움 극복 순간, 꿈의 좌절, 꿈의 변화, 인생의 터닝포인트
- 감정/취향: 좋아하는 것, 두려운 것, 몰입 경험, 감탄한 순간, 나만의 위로방식
- 사회/문화: 여행 경험, 세대 간 갈등, 종교 참여, 사회적 사건

**조건:**
- 진행 중인 주제(title)와 subtitle은 변경하지 않고 그대로 출력
- subtitle에 맞는 새로운 subtopic_description을 작성

응답은 아래 JSON 형식으로 출력:
```json
{{
  "title": {{title}},  # Redis 진행상황에서 유지된 title
  "subtitle": {{subtitle}},  # Redis 진행상황에서 유지된 subtitle
  "subtopic": {{subtopic}},
  "response": "짧은 호응 한마디 (질문 포함 X)",
  "question": "다음 인터뷰 질문 (질문 문장만)",
}}
"""
)

# LLM 하위 질문 생성 Prompt
subquestion_prompt = PromptTemplate.from_template("""
당신은 사용자의 자서전을 돕는 인터뷰 질문 생성 AI입니다.

사용자가 최근에 다음 질문에 답변했습니다:
"{parent_question}"
사용자 답변:
"{answer}"

관련 참고 문서:
{context}

이제 사용자가 좀 더 깊이 있는 대화를 이어갈 수 있도록, 해당 질문에 대해 추가적으로 묻고 싶은 하위 질문 3~5개를 생성해 주세요.
하위 질문은 너무 길거나 복잡하지 않게, 자연스럽고 구체적인 내용으로 작성해 주세요.

**조건:**
- 사용자의 이전 답변과 중복되지 않은 새로운 질문
- 질문은 한 번에 하나만 묻고 너무 길거나 복잡하지 않게 작성
- 질문은 감정, 동기, 배경, 맥락까지 자연스럽게 이어지도록 작성
- 질문이 끝나면, 새로운 주제로 넘어가자고 제안할 수도 있음 ("혹시 이번엔 다른 주제로 넘어가볼까?" 등)
- 호응과 다음 질문 모두 출력할 것

```json
{{
  "response": "짧은 호응 한마디 (질문 포함 X)",
  "question": "다음 인터뷰 질문 (질문 문장만)",
  "is_continue": true, # 사용자가 현재 주제를 계속 이야기할지 여부
  "is_next": true,
  "is_over": false
}}
""")
