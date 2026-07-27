from pathlib import Path

from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from pydantic import BaseModel, ValidationError

from settings import Settings
from database import Database
from vector_database import VectorDatabase, build_final_prompt
from message_repository import MessageRepository
from message_model import MessageCreate, Message
from ollama_model import OllamaModel, get_last_assistant_message

db = Database(url=Settings.DB_URL, echo=Settings.DB_ECHO)

ollama_model = OllamaModel(
    api_key=Settings.OLLAMA_KEY, model=Settings.LLM_MODEL)
vector_database = VectorDatabase.build_from_settings(settings=Settings)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

SYSTEM_PROMPT = Path("system_prompt.md").read_text(encoding="utf-8")


def get_message_repository(session: Session = Depends(db.get_session)) -> MessageRepository:
    return MessageRepository(session=session)


def get_ollama_model() -> OllamaModel:
    return ollama_model


def get_vector_db() -> VectorDatabase:
    return vector_database


class UserRequest(BaseModel):
    prompt: str


@app.websocket("/chat")
async def chat(
    websocket: WebSocket,
    ollama: OllamaModel = Depends(get_ollama_model),
    vector_db: VectorDatabase = Depends(get_vector_db),
    repo: MessageRepository = Depends(get_message_repository)
):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_json()

            try:
                data = UserRequest.model_validate(raw)

                prompt = data.prompt

                await run_in_threadpool(repo.create, "user", prompt)

                recent_messages = await run_in_threadpool(repo.get_some)

                history = [{"role": msg.role.value, "content": msg.content}
                           for msg in recent_messages]

                last_response = get_last_assistant_message(history)

                user_chunks = await run_in_threadpool(vector_db.search, prompt, 3, 0.54)
                assistant_chunks = await run_in_threadpool(vector_db.search, last_response["content"], 3, 0.54) if last_response else []

                FINAL_SYSTEM_PROMPT = build_final_prompt(
                    SYSTEM_PROMPT, user_chunks, assistant_chunks)

                full_response = ""

                async for part in ollama.send_messages([
                        {"role": "system", "content": FINAL_SYSTEM_PROMPT},
                    *history
                ]):
                    full_response += part
                    await websocket.send_json({"type": "part", "content": part})

                await run_in_threadpool(repo.create, "assistant", full_response)

                await websocket.send_json({"type": "done"})
            except ValidationError:
                await websocket.send_json({"type": "error ", "content": "Invalid request body"})

    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/messages/")
def get_messages(repo: MessageRepository = Depends(get_message_repository), limit: int = 10):
    return repo.get_some(limit=limit)


@app.get("/messages/all")
def get_all_messages(repo: MessageRepository = Depends(get_message_repository)):
    return repo.get_all()
