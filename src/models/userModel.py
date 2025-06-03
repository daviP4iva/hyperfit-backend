from pydantic import BaseModel, EmailStr
from enum import Enum

class Message(BaseModel):
    role: str
    content: str

class LevelEnum(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class GoalEnum(str, Enum):
    lose_weight = "lose_weight"
    gain_muscle = "gain_muscle"
    maintain = "maintain"
    define = "define"

class User(BaseModel):
    _id: str
    name: str
    email: EmailStr
    password: str | None = None
    height: int | None = None
    weight: int | None = None
    level: LevelEnum | None = None
    goal: GoalEnum | None = None
    allergens: str | None = None
    google_id: str | None = None
    history: list[Message] = []