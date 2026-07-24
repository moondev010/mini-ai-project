from typing import Iterator

from ollama import Client


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

        self._client = Client(
            host=host,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    def send_messages(self, messages: list[dict]) -> Iterator[str]:
        stream = self._client.chat(
            model=self._model,
            messages=messages,
            think=self._think,
            stream=True
        )

        for part in stream:
            yield part["message"]["content"]
