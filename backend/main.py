from fastapi import FastAPI, Depends
from sqlmodel import Session

from settings import Settings
from database import Database
from message_repository import MessageRepository
from message_model import MessageCreate

db = Database(url=Settings.DB_URL, echo=Settings.DB_ECHO)

app = FastAPI()


def get_message_repository(session: Session = Depends(db.get_session)) -> MessageRepository:
    return MessageRepository(session=session)


@app.post("/messages/")
def create_message(data: MessageCreate, repo: MessageRepository = Depends(get_message_repository)):
    return repo.create(role=data.role, content=data.content)


@app.get("/messages/")
def get_all_messages(repo: MessageRepository = Depends(get_message_repository), limit: int = 10):
    return repo.get_some(limit=limit)


@app.get("/messages/all")
def get_all_messages(repo: MessageRepository = Depends(get_message_repository)):
    return repo.get_all()
