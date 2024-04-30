from fastapi import HTTPException
from jose import JWTError
from starlette import status
from app.services.companies import CompanyService
from app.services.users import UserService
from app.repository.actions import ActionsRepository
import app.schemas.actions as action_schema
from app.utils.utils import decode_access_token
from app.db.company import RequestType, Status


class ActionService:
    def __init__(self, session, token):
        self.session = session
        self.token = token

    async def owner_validation(self, company_id: int):
        """Validating that user is company owner. And returns company-owner pair"""
        try:
            token_user_id, token_email, token_username = decode_access_token(self.token.credentials)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')
        company, owner = await CompanyService(self.session, self.token).get_company_details(company_id)
        if owner.email != token_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        return company, owner

    async def get_current_user(self):
        """Get real user id from database here"""
        try:
            token_user_id, token_email, token_username = decode_access_token(self.token.credentials)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')
        current_user = await UserService(self.session).user_details_by_email(token_email)
        return current_user

    async def member_validation(self, user_id: int):
        """Check permissions of member"""
        user = await self.get_current_user()
        if user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        return user

    async def create_action(self, request_body: action_schema.ActionCreateRequest) -> action_schema.ActionResponse:
        """Checking access based on request type. Creating action if user is validated."""
        company_id = request_body.company_id
        user_id = request_body.user_id
        if request_body.request_type == RequestType.INVITATION:
            company, owner = await self.owner_validation(company_id)
            user = await UserService(self.session).user_details_by_id(user_id)
        else:
            user = await self.member_validation(user_id)
            company, owner = await CompanyService(self.session).get_company_details(company_id)
        #  Check that user is not a member of a company
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
        action = await self.get_action(action_id)
        user = await self.get_current_user()
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
        user = await self.get_current_user()
        if action.request_type == RequestType.REQUEST and user.id != action.user_id or\
                action.request_type == RequestType.INVITATION and user.id != action.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        await ActionsRepository(self.session).delete_action(action_id)
        return action.request_type

    async def get_actions(self, action_type: RequestType):
        """Get all actions for current user"""
        user = await self.get_current_user()
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

    async def get_all_members(self, company_id):
        """get all members of a company
        need to check that token id == company owner id"""

    async def remove_member(self, delete_request, company_id):  # delete request has user id and company id
        """need to validate either token_id == user_id from request OR company_owner_id == token_id"""
