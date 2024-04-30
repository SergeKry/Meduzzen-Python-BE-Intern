from sqlalchemy import select, delete

import app.db.company as db_model
import app.db.user as user_model
from app.schemas import actions as action_schema
from app.db.company import Status


class ActionsRepository:
    def __init__(self, session):
        self.session = session
        self.action_model = db_model.Action
        self.company_model = db_model.Company
        self.user_model = user_model.User

    async def create_action(self, action: action_schema.ActionCreateRequest):
        new_action = self.action_model(**action.dict(), status=Status.PENDING)
        self.session.add(new_action)
        await self.session.commit()
        return new_action

    async def get_action_duplicate(self, company_id: int, user_id: int, request_type: db_model.RequestType):
        query = select(self.action_model)\
            .filter(self.action_model.company_id == company_id)\
            .filter(self.action_model.user_id == user_id)\
            .filter(self.action_model.request_type == request_type)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def get_action_by_id(self, action_id: int):
        """Returns action_id, user_id, action request_type, company_owner_id"""
        query = select(self.action_model.id, self.action_model.user_id, self.action_model.request_type,
                       self.company_model.owner_id)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .filter(self.action_model.id == action_id)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def delete_action(self, action_id: int):
        stmt = delete(self.action_model).where(self.action_model.id == action_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_actions(self, user_id, request_type: db_model.RequestType):
        query = select(self.action_model.id, self.company_model.name, self.user_model.username, self.action_model.status)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .join(self.user_model, self.user_model.id == self.action_model.user_id)\
            .filter(self.action_model.request_type == request_type)\
            .filter(self.action_model.user_id == user_id)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def get_company_actions(self, company_id: int, request_type: db_model.RequestType):
        query = select(self.action_model.id, self.company_model.name, self.user_model.username,self.action_model.status)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id) \
            .join(self.user_model, self.user_model.id == self.action_model.user_id)\
            .filter(self.action_model.request_type == request_type)\
            .filter(self.action_model.company_id == company_id)
        query_result = await self.session.execute(query)
        return query_result.all()