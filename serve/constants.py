from enum import Enum

class Gender(Enum):
  MALE = "MALE"
  FEMALE = "FEMALE"
  NONE = "NONE"


class ConversationType(Enum):
  BOT = "BOT"
  HUMAN = "HUMAN"
