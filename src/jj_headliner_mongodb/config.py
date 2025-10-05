from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Final
from urllib.parse import urlencode

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import MongoClient

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping

    from pymongo.synchronous.database import Database

_DB_COLL_LATEST_NEWS_FLOW_RUNS: Final[str] = "latest-news-flow-runs"
_DB_COLL_LATEST_NEWS_RESULT_PAGE: Final[str] = "latest-news-result-pages"

_NOT_SET: Final[str] = "<not_set>"


class MongoConfig(BaseSettings):
    _PARAMS_DEFAULT: Final[Mapping[str, str]] = {
        "retryWrites": "true",
        "w": "majority",
    }
    model_config = SettingsConfigDict(
        env_file=".mongodb.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    host: str = _NOT_SET
    user: str = _NOT_SET
    password: str = _NOT_SET

    db_name: str = _NOT_SET

    app_name: str | None = None

    coll_latest_news_flow_runs: str = _DB_COLL_LATEST_NEWS_FLOW_RUNS
    coll_latest_news_result_page: str = _DB_COLL_LATEST_NEWS_RESULT_PAGE

    @computed_field
    @property
    def connection_string(self) -> str:
        params = {**self._PARAMS_DEFAULT, "appName": self.app_name} if self.app_name else self._PARAMS_DEFAULT
        return f"mongodb+srv://{self.user}:{self.password}@{self.host}/?{urlencode(params)}"


@contextmanager
def mongo_db(mongo_config: MongoConfig) -> Generator[Database, None, None]:
    with MongoClient(mongo_config.connection_string) as client:
        yield client.get_database(mongo_config.db_name)
