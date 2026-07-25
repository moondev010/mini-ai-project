from pathlib import Path

from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlmodel import Session

from settings import Settings
from database import Database
from message_repository import MessageRepository
from message_model import MessageCreate
from ollama_model import OllamaModel

db = Database(url=Settings.DB_URL, echo=Settings.DB_ECHO)
ollama_model = OllamaModel(
    api_key=Settings.OLLAMA_KEY, model=Settings.LLM_MODEL)

app = FastAPI()

SYSTEM_PROMPT = Path("system_prompt.md").read_text(encoding="utf-8")


def get_message_repository(session: Session = Depends(db.get_session)) -> MessageRepository:
    return MessageRepository(session=session)


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            prompt = await websocket.receive_text()

            async for part in ollama_model.send_messages([
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]):
                await websocket.send_json({"type": "part", "content": part})

            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/messages/")
def create_message(data: MessageCreate, repo: MessageRepository = Depends(get_message_repository)):
    return repo.create(role=data.role, content=data.content)


@app.get("/messages/")
def get_messages(repo: MessageRepository = Depends(get_message_repository), limit: int = 10):
    return repo.get_some(limit=limit)


@app.get("/messages/all")
def get_all_messages(repo: MessageRepository = Depends(get_message_repository)):
    return repo.get_all()
