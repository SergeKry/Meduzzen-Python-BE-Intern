from fastapi import APIRouter, HTTPException
from starlette import status
from app.routers.routers import db_dependency, token_dependency
from app.schemas import actions as act_schema
from app.schemas import companies as comp_schema
from app.services.actions import ActionService as ActServ
from app.db.company import RequestType, Status

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


@action_router.patch("/action/{action_id}", response_model=act_schema.ActionResponse, tags=["Actions"])  # this is to accept/decline
async def accept_decline_action(action_id: int, request_body: act_schema.ActionUpdateRequest,
                        session: db_dependency, token: token_dependency):
    requested_status = request_body.status
    if requested_status == Status.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status can be either Accepted or Declined")
    updated_action = await ActServ(session, token).update_action(action_id, requested_status)
    return updated_action


@action_router.delete("/action/{action_id}", tags=["Actions"])
async def delete_action(action_id: int, session: db_dependency, token: token_dependency):
    action_type = await ActServ(session, token).delete_action(action_id)
    return {"message": f"{action_type.value} deleted"}


@action_router.get("/members/{company_id}", response_model=comp_schema.MemberList, tags=['Members'])
async def get_company_members(company_id: int, session: db_dependency, token: token_dependency):
    members = await ActServ(session, token).get_all_members(company_id)
    return members


@action_router.patch("/members/{company_id}", tags=['Members'])
async def change_user_role(request_body: comp_schema.MemberRoleUpdateRequest,
                           company_id: int, session: db_dependency, token: token_dependency):
    await ActServ(session, token).update_role(company_id, request_body)
    return {"message": "Role updated"}


@action_router.delete("/members/{company_id}", tags=['Members'])
async def remove_member(delete_request: comp_schema.MemberDeleteRequest, company_id: int,
                        session: db_dependency, token: token_dependency):
    await ActServ(session, token).remove_member(delete_request, company_id)
    return {"message": "User deleted"}
