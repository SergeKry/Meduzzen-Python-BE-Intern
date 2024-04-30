from fastapi import APIRouter
from starlette import status
from app.routers.routers import db_dependency, token_dependency
from app.schemas import actions as act_schema
from app.schemas import companies as comp_schema
from app.services.actions import ActionService as ActServ
from app.db.company import RequestType

action_router = APIRouter()


@action_router.post("/action/",
                    response_model=act_schema.ActionResponse, status_code=status.HTTP_201_CREATED, tags=["Actions"])
async def create_action(request: act_schema.ActionCreateRequest, session: db_dependency, token: token_dependency):
    new_action = await ActServ(session, token).create_action(request)
    return new_action


@action_router.get("/action/my_invitations", response_model=act_schema.ActionListResponse, tags=["Actions"])
async def get_users_invitations(session: db_dependency, token: token_dependency):
    action_type = RequestType.INVITATION
    actions = await ActServ(session, token).get_actions(action_type)
    return act_schema.ActionListResponse(type=action_type, actions=actions)


@action_router.get("/action/my_requests", response_model=act_schema.ActionListResponse, tags=["Actions"])
async def get_users_requests(session: db_dependency, token: token_dependency):
    action_type = RequestType.REQUEST
    actions = await ActServ(session, token).get_actions(action_type)
    return act_schema.ActionListResponse(type=action_type, actions=actions)


@action_router.get("/action/company_invites/{company_id}", response_model=act_schema.ActionListResponse,
                   tags=["Actions"])
async def get_company_invitations(company_id: int, session: db_dependency, token: token_dependency):
    action_type = RequestType.INVITATION
    actions = await ActServ(session, token).get_company_actions(company_id, action_type)
    return act_schema.ActionListResponse(type=action_type, actions=actions)


@action_router.get("/action/company_requests/{company_id}", response_model=act_schema.ActionListResponse,
                   tags=["Actions"])
async def get_company_requests(company_id: int, session: db_dependency, token: token_dependency):
    action_type = RequestType.REQUEST
    actions = await ActServ(session, token).get_company_actions(company_id, action_type)
    return act_schema.ActionListResponse(type=action_type, actions=actions)


@action_router.patch("/action/{action_id}", tags=["Actions"])  # this is to accept/decline
async def update_action(action_id: int, request_body,
                        session: db_dependency, token: token_dependency):
    await ActServ(session, token).update_action(action_id, request_body)
    # return updated here


@action_router.delete("/action/{action_id}", tags=["Actions"])
async def delete_action(action_id: int, session: db_dependency, token: token_dependency):
    action_type = await ActServ(session, token).delete_action(action_id)
    return {"message": f"{action_type.value} deleted"}


@action_router.get("/members/{company_id}",
                   response_model=comp_schema.MemberList, tags=['Members'])
async def get_company_members(company_id: int, session: db_dependency, token: token_dependency):
    await ActServ(session, token).get_all_members(company_id)
    #  return list of members


@action_router.delete("/members/{company_id}", tags=['Members'])
async def remove_member(delete_request: comp_schema.MemberDeleteRequest, company_id: int,
                        session: db_dependency, token: token_dependency):
    await ActServ(session, token).remove_member(delete_request, company_id)
    #  need to return some confirmation
