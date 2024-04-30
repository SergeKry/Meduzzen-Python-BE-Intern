from fastapi import HTTPException
from jose import JWTError
from starlette import status
from app.services.companies import CompanyService
from app.services.users import UserService
from app.repository.actions import ActionsRepository
import app.schemas.actions as action_schema
from app.utils.utils import decode_access_token
from app.db.company import RequestType


class ActionService:
    def __init__(self, session, token):
        self.session = session
        self.token = token

    async def owner_validation(self, company_id: int):
        """Validating that user is company owner. And returns company, owner pair"""
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
        """Check permissions of user"""
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
        #  Check if such invitation does not exist
        action = await ActionsRepository(self.session).create_action(request_body)
        return action_schema.ActionResponse(action_id=action.id, company_name=company.name,
                                            username=user.username, request_type=request_body.request_type)

    async def update_action(self, action_id, request_body):
        """We need to get action from db first to check status
        if type == invitation, check that company owner == token (via func)
        if type == request, check that requester id = token id (via func)
        Than change only accept or decline"""

    async def delete_action(self, action_id):
        """if type == invitation, check that company owner == token (via func)
        if type == request, check that requester id = token id (via func)
        Than delete an action"""

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
