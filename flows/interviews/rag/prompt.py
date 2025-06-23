import os
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
import pandas as pd

initial_prompt = PromptTemplate.from_template("""
사용자가 준 첫 응답을 바탕으로 다음을 선택하세요:
- title: 전체 주제 (필수. 반드시 아래 리스트에서 선택)
- subtitle: 소주제 (필수. 반드시 해당 title 아래에서 선택)
- subtopic: subtitle을 기반으로 한 구체적 이야기 포인트 (subtitle의 하위 질문 느낌)
- subtopics: 같은 subtitle에 속하는 관련 subtopic들의 리스트 (최소 3개 이상, 첫 subtopic 포함)
- reason: 왜 그렇게 선택했는지에 대한 이유 (사용자 응답과의 연결 설명)

다음은 사용자의 첫 응답입니다:
"{answer}"

사용자에 대한 추가 정보:
- 연령대: {age_group}
- 성별: {gender}
- 학력: {education_level}
- 결혼 여부: {marital_status}

사용자의 과거 대화 히스토리:
{chat_history}

다음은 선택 가능한 title / subtitle 리스트입니다. 반드시 여기에서만 선택하세요:

- 성장과정: 출생, 첫 독립, 첫 실패, 부모와의 거리감
- 가족관계: 부모, 형제자매, 자녀, 조부모, 반려동물, 배우자
- 학창시절: 학교 생활, 친구 관계, 과목 수업, 동아리 활동
- 직업/진로: 진로 선택 계기, 업무 에피소드, 대외활동, 번아웃 경험
- 가치관/성격: 성격 변화, 신념 형성 계기, 철학적 사고, 인생의 전환점
- 인생 경험: 어려움 극복 순간, 꿈의 좌절, 꿈의 변화, 인생의 터닝포인트
- 감정/취향: 좋아하는 것, 두려운 것, 몰입 경험, 감탄한 순간, 나만의 위로방식
- 사회/문화: 여행 경험, 세대 간 갈등, 종교 참여, 사회적 사건

다음은 각 subtitle에 대한 추천 가능한 subtopic 리스트입니다. 반드시 이 범위에서 선택하거나 유사하게 작성하세요:
{questions_meta}

응답 형식은 반드시 다음과 같이 JSON으로 출력하세요 (key 이름 및 형식 모두 철저히 지켜야 합니다):

```json
{{
  "title": "{{title}}",
  "subtitle": "{{subtitle}}",
  "subtopic": "{{subtopic}}",
  "subtopics": ["{{subtopic}}", "...", "..."],
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

**조건:**
- 진행 중인 주제(title)와 subtitle은 변경하지 않고 그대로 출력
- subtitle에 맞는 새로운 subtopic_description을 작성

응답은 아래 JSON 형식으로 출력:
```json
{{
  "title": {title},  # Redis 진행상황에서 유지된 title
  "subtitle": {subtitle},  # Redis 진행상황에서 유지된 subtitle
  "subtopic": {subtopic},
  "response": "짧은 호응 한마디 (질문 포함 X)",
  "question": "다음 인터뷰 질문 (질문 문장만)",
}}
"""
)

# LLM 하위 질문 생성 Prompt
subquestion_prompt = PromptTemplate.from_template("""
당신은 자서전 인터뷰를 돕는 따뜻하고 공감 능력이 뛰어난 AI입니다.

다음은 사용자가 방금 답변한 질문과 그에 대한 응답입니다:
질문: "{parent_question}"
답변: "{answer}"

이 사용자의 이전 대화 흐름은 다음과 같습니다:
{context}

이제 이 사용자의 이야기를 더 깊이 있게 이끌어주세요.

**목표**:
- 공감하는 짧은 리액션 (`response`) 생성
- 감정, 동기, 기억 등을 더 자세히 이끌어내는 후속 질문 (`question`) 생성
- 추가로 물어볼 수 있는 하위 질문 (`subquestions`) 리스트도 함께 제공

**주의사항**:
- response는 인간적인 감정 표현이 담겨야 함 (질문 포함 X)
- question은 인터뷰의 연속 흐름처럼, 감정과 배경을 고려해 자연스럽게 작성
- subquestions는 3~5개, 사용자의 감정을 깊이 있게 탐색하거나 다른 각도를 제시하는 질문이어야 함

다음 JSON 형식으로 출력하세요:

```json
{{
  "response": "짧은 공감 리액션",
  "question": "후속 질문 (문장 끝에 물음표 포함)",
  "is_continue": true,
  "is_next": true,
  "is_over": false,
  "subquestions": [
    "하위 질문 1",
    "하위 질문 2",
    "하위 질문 3"
  ]
}}
""")
