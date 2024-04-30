from typing import List

from pydantic import BaseModel, Field
from app.db.company import RequestType, Status


class Action(BaseModel):
    id: int
    company_id: int
    user_id: int
    status: Status


class ActionCreateRequest(BaseModel):
    company_id: int
    user_id: int
    request_type: RequestType


class ActionResponse(BaseModel):
    action_id: int
    company_name: str
    username: str
    status: Status


class ActionListResponse(BaseModel):
    type: RequestType
    actions: List[ActionResponse]


class ActionUpdateRequest(BaseModel):
    status: Status
