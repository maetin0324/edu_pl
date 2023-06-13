from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    user = "user"
    assistant = "assistant"

class AnswerBase(BaseModel):
    role: Role
    content: str

class ProblemBase(BaseModel):
    initial_prompt: str
    messages: List[AnswerBase]

