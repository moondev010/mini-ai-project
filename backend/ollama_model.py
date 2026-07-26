from typing import AsyncIterator

from ollama import AsyncClient


class OllamaModel:
    def __init__(
        self,
        api_key: str | None,
        model: str = "gpt-oss:20b-cloud",
        host: str = "https://ollama.com",
        think: str | bool = "medium",
    ):
        self._model = model
        self._host = host
        self._think = think

        self._client = AsyncClient(
            host=host,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def send_messages(self, messages: list[dict]) -> AsyncIterator[str]:
        stream = await self._client.chat(
            model=self._model,
            messages=messages,
            think=self._think,
            stream=True
        )

        async for part in stream:
            if part["message"]["content"] != "":
                yield part["message"]["content"]


def get_last_assistant_message(history: list[dict]):
    for msg in reversed(history[:-1]):
        if msg["role"] == "assistant":
            return msg

    return None
