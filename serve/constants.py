from enum import Enum


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NONE = "NONE"


class ConversationType(Enum):
    BOT = "BOT"
    HUMAN = "HUMAN"


class MemberRole(Enum):
    PRE_MEMBER = "PRE_MEMBER"
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
