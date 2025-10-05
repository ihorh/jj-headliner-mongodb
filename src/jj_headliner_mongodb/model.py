from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

if TYPE_CHECKING:
    from datetime import datetime

    from bson import ObjectId


class FetchNewsFlowDoc(TypedDict):
    _id: ObjectId
    started: datetime
    max_pages: int
    dry_run: bool
    prefect_flow_context: PrefectFlowContextDoc


class FetchNewsResultPageDoc(TypedDict):
    _id: NotRequired[ObjectId]
    _fetch_news_flow_doc_id: ObjectId  # * "n:1 foreign key"
    country_and_lang: str
    page_num: int
    request_params: dict[str, Any]
    articles: list[dict[str, Any]]


class PrefectFlowContextDoc(TypedDict):
    flow_name: str
    flow_run_name: str
    flow_run_id: str | None
    flow_run_started: datetime
