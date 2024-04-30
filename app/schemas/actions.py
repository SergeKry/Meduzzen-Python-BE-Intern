from typing import List

from pydantic import BaseModel, Field
from app.db.company import RequestType


class Action(BaseModel):
    id: int
    company_id: int
    user_id: int
    status: str


class ActionCreateRequest(BaseModel):
    company_id: int
    user_id: int
    request_type: RequestType


class ActionResponse(BaseModel):
    action_id: int
    company_name: str
    username: str
    request_type: RequestType


class ActionListResponse(BaseModel):
    type: str
    actions: List[ActionResponse]


class ActionUpdateRequest(BaseModel):
    status: str
