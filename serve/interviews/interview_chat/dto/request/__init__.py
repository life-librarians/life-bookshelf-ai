from typing import List

from pydantic import BaseModel, Field
from datetime import date

from constants import Gender, ConversationType


class UserInfoDto(BaseModel):
    user_name: str = Field(default="최시원")
    date_of_birth: date = Field(default="2000-02-21")
    gender: Gender = Field(default=Gender.FEMALE)
    has_children: bool = Field(default=False)
    occupation: str = Field(default="프로그래머")
    education_level: str = Field(default="대학교 재학")
    marital_status: str = Field(default="미혼")


class ChapterInfoDto(BaseModel):
    title: str = Field(default="20대")
    description: str = Field(default="대학 생활과 첫 직장 경험")


class SubChapterInfoDto(BaseModel):
    title: str = Field(default="첫 직장 생활")
    description: str = Field(default="소프트웨어 회사에서의 첫 직장 경험과 적응 과정")


class InterviewConversationHistoryDto(BaseModel):
    content: str = Field(
        default="회사에서 맡은 첫 프로젝트는 무엇이었고, 어떤 도전이 있었나요?"
    )
    conversation_type: ConversationType = Field(default=ConversationType.BOT)


class InterviewChatRequestDto(BaseModel):
    user_info: UserInfoDto = Field(default_factory=UserInfoDto)
    chapter_info: ChapterInfoDto = Field(default_factory=ChapterInfoDto)
    sub_chapter_info: SubChapterInfoDto = Field(default_factory=SubChapterInfoDto)
    conversation_history: List[InterviewConversationHistoryDto] = Field(
        default=[
            InterviewConversationHistoryDto(),
            InterviewConversationHistoryDto(
                content="긴장도 되고 설렘도 있었어요. 새로운 환경에 적응해야 한다는 부담감도 있었지만, 제가 배운 것을 실제로 적용할 수 있다는 기대감이 컸죠.",
                conversation_type=ConversationType.HUMAN,
            ),
            InterviewConversationHistoryDto(
                content="첫 프로젝트에 참여하셨을 때, 어떤 역할을 맡으셨고 어떤 어려움이 있었나요?",
                conversation_type=ConversationType.BOT,
            ),
            InterviewConversationHistoryDto(
                content="주니어 개발자로 팀에 합류해서 기존 애플리케이션의 일부 기능을 개선하는 작업을 맡았어요. 처음에는 큰 코드베이스를 이해하는 게 어려웠고, 팀의 코딩 스타일에 적응하는 데도 시간이 걸렸죠.",
                conversation_type=ConversationType.HUMAN,
            ),
            InterviewConversationHistoryDto(
                content="회사 생활을 하면서 대학에서 배운 것과 실제 업무 사이에 어떤 차이를 느끼셨나요?",
                conversation_type=ConversationType.BOT,
            ),
            InterviewConversationHistoryDto(
                content="대학에서는 주로 이론과 작은 프로젝트에 집중했다면, 실제 업무는 훨씬 복잡하고 규모가 컸어요. 특히 팀워크와 의사소통의 중요성을 실감했고, 버전 관리나 코드 리뷰 같은 실무적인 기술들을 새로 배워야 했죠.",
                conversation_type=ConversationType.HUMAN,
            ),
            InterviewConversationHistoryDto(
                content="직장 생활을 하면서 일과 삶의 균형을 유지하는 데 어려움은 없으셨나요?",
                conversation_type=ConversationType.BOT,
            ),
            InterviewConversationHistoryDto(
                content="처음에는 좀 힘들었어요. 업무에 적응하느라 야근도 자주 하고, 주말에도 공부를 더 해야 한다는 부담감이 있었거든요. 하지만 점차 시간 관리 능력이 늘면서 개인 시간도 가질 수 있게 되었어요.",
                conversation_type=ConversationType.HUMAN,
            ),
            InterviewConversationHistoryDto(
                content="첫 직장에서의 경험이 앞으로의 커리어 계획에 어떤 영향을 미쳤나요?",
                conversation_type=ConversationType.BOT,
            ),
        ],
    )
    current_answer: str = Field(
        default="제가 정말 프로그래밍을 좋아한다는 걸 확신하게 되었어요. 특히 팀원들과 협력해서 문제를 해결하는 과정이 즐거웠죠. 앞으로는 더 전문성을 키워서 시니어 개발자로 성장하고 싶다는 목표가 생겼어요."
    )
    question_limit: int = Field(default=5)
