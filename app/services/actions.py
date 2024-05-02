from urllib import request

from fastapi import HTTPException
from starlette import status
from app.services.companies import CompanyService
from app.services.users import UserService
from app.repository.actions import ActionsRepository
import app.schemas.actions as action_schema
import app.schemas.companies as company_schema
from app.db.company import RequestType, Status, RoleName


class ActionService:
    def __init__(self, session, token):
        self.session = session
        self.token = token

    async def owner_validation(self, company_id: int):
        """Validation for create action. User should be company owner. Func returns company-owner pair"""
        user = await UserService(self.session).get_current_user(self.token)
        company, owner = await CompanyService(self.session, self.token).get_company_details(company_id)
        if owner.id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        return company, owner, user

    async def member_validation(self, user_id: int):
        """Check permissions of member for creating a membership request"""
        user = await UserService(self.session).get_current_user(self.token)
        if user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        return user

    async def check_existing_member(self, company_id: int, user_id: int):
        """Check to avoid member duplicates inside a company"""
        member = await ActionsRepository(self.session).get_member_by_id(user_id, company_id)
        if member:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already in the company')

    async def create_action(self, request_body: action_schema.ActionCreateRequest) -> action_schema.ActionResponse:
        """Check access based on request type. Creating action if user is validated."""
        company_id = request_body.company_id
        user_id = request_body.user_id
        await self.check_existing_member(company_id, user_id)
        if request_body.request_type == RequestType.INVITATION:
            company, owner, user = await self.owner_validation(company_id)
        else:
            user = await self.member_validation(user_id)
            company, owner = await CompanyService(self.session).get_company_details(company_id)
        if await ActionsRepository(self.session).get_action_duplicate(company_id, user_id, request_body.request_type,
                                                                      Status.PENDING):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User Already invited')
        action = await ActionsRepository(self.session).create_action(request_body)
        return action_schema.ActionResponse(action_id=action.id, company_name=company.name,
                                            username=user.username, status=action.status)

    async def get_action(self, action_id: int):
        action = await ActionsRepository(self.session).get_action_by_id(action_id)
        if not action:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Action not found')
        return action

    async def update_action(self, action_id, new_status: Status) -> action_schema.ActionResponse:
        """Accept or decline invitations/requests"""
        action = await self.get_action(action_id)
        user = await UserService(self.session).get_current_user(self.token)
        if action.request_type == RequestType.REQUEST and user.id == action.user_id or\
                action.request_type == RequestType.INVITATION and user.id == action.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        if action.status != Status.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{action.request_type.value} is closed')
        await ActionsRepository(self.session).update_action(action_id, new_status)
        if new_status == Status.ACCEPTED:
            await ActionsRepository(self.session).add_member(action.company_id, action.user_id)
        updated_action = await ActionsRepository(self.session).get_action_details(action_id)
        return action_schema.ActionResponse(action_id=updated_action.id,
                                            company_name=updated_action.name,
                                            username=updated_action.username,
                                            status=updated_action.status)

    async def delete_action(self, action_id):
        """Delete action if exists"""
        action = await self.get_action(action_id)
        user = await UserService(self.session).get_current_user(self.token)
        if action.request_type == RequestType.REQUEST and user.id != action.user_id or\
                action.request_type == RequestType.INVITATION and user.id != action.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        await ActionsRepository(self.session).delete_action(action_id)
        return action.request_type

    async def get_actions(self, action_type: RequestType):
        """Get all actions for current user"""
        user = await UserService(self.session).get_current_user(self.token)
        actions = await ActionsRepository(self.session).get_user_actions(user.id, action_type)
        actions_list = [action_schema.ActionResponse(action_id=action.id,
                                                     company_name=action.name,
                                                     username=action.username,
                                                     status=action.status) for action in actions]
        return actions_list

    async def get_company_actions(self, company_id: int, action_type):
        """Get all actions for specified company"""
        await self.owner_validation(company_id)
        actions = await ActionsRepository(self.session).get_company_actions(company_id, action_type)
        actions_list = [action_schema.ActionResponse(action_id=action.id,
                                                     company_name=action.name,
                                                     username=action.username,
                                                     status=action.status) for action in actions]
        return actions_list

    async def get_all_members(self, company_id) -> company_schema.MemberList:
        """Get all members of a company. Validation is made for company owner"""
        members = await ActionsRepository(self.session).get_all_members(company_id)
        if not members:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        owner = await UserService(self.session).get_current_user(self.token)
        if owner.id != members[0].user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        members_list = [company_schema.Member(username=member.username, role=member.role_name) for member in members]
        return company_schema.MemberList(members=members_list)

    async def remove_member(self, delete_request, company_id: int) -> None:
        """Remove member. Member can remove himself OR owner can remove a member. Owner can't be removed at all"""
        member = await ActionsRepository(self.session).get_member_by_id(delete_request.user_id, company_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found')
        current_user = await UserService(self.session).get_current_user(self.token)
        company, owner = await CompanyService(self.session).get_company_details(company_id)
        if member.user_id != current_user.id and owner.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        if member.user_id == current_user.id and owner.id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Can\'t delete owner')
        await ActionsRepository(self.session).delete_member(delete_request.user_id, company_id)

    async def update_role(self, company_id: int, request_body: company_schema.MemberRoleUpdateRequest):
        """available only for owner. Owners role cant be updated"""
        if request_body.role == RoleName.OWNER:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Can\'t change the owner')
        company, owner, current_user = await self.owner_validation(company_id)
        if owner.id == request_body.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Can\'t change owner\'s role')
        role = await ActionsRepository(self.session).get_role_by_rolename(request_body.role)
        await ActionsRepository(self.session).update_member(company_id, request_body.user_id, role.id)
