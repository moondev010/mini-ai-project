from typing import Generator, Any
from sqlmodel import create_engine, Session, SQLModel


class Database:
    def __init__(self, url: str, echo: bool = False):
        self._engine = create_engine(url, echo=echo)

    def init_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    def get_session(self) -> Generator[Session, Any, None]:
        with Session(self._engine) as session:
            yield session
