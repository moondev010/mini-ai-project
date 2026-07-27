from sqlmodel import select, Session

from typing import Sequence

from database import Database
from message_model import Message, Role


class MessageRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, role: Role, content: str) -> Message:
        message = Message(role=role, content=content)
        self._session.add(message)
        self._session.commit()
        self._session.refresh(message)
        return message

    def get_all(self) -> Sequence[Message]:
        statement = select(Message).order_by(Message.created_at.desc())

        return list(reversed(self._session.exec(statement).all()))

    def get_some(self, limit: int = 10) -> Sequence[Message]:
        statement = select(Message).order_by(
            Message.created_at.desc()).limit(limit)

        return list(reversed(self._session.exec(statement).all()))
