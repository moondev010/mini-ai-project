from datetime import datetime
from sqlmodel import Field, SQLModel
from enum import Enum


class Role(str, Enum):
    USER = "user",
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: Role
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
