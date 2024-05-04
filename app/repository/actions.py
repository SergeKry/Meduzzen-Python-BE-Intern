from sqlalchemy import select, delete, update
import app.db.company as db_model
import app.db.user as user_model
from app.schemas import actions as action_schema
from app.db.company import Status, RoleName


class ActionsRepository:
    def __init__(self, session):
        self.session = session
        self.action_model = db_model.Action
        self.company_model = db_model.Company
        self.user_model = user_model.User
        self.member_model = db_model.CompanyMember
        self.role_model = db_model.CompanyRole

    async def create_action(self, action: action_schema.ActionCreateRequest):
        new_action = self.action_model(**action.dict(), status=Status.PENDING)
        self.session.add(new_action)
        await self.session.commit()
        return new_action

    async def get_action_duplicate(self, company_id: int, user_id: int, request_type: db_model.ActionType,
                                   status: Status):
        query = select(self.action_model)\
            .filter(self.action_model.company_id == company_id)\
            .filter(self.action_model.user_id == user_id)\
            .filter(self.action_model.request_type == request_type)\
            .filter(self.action_model.status == status)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def get_action_by_id(self, action_id: int):
        """Returns action_id, user_id, action request_type, company_owner_id, action_status, company_id"""
        query = select(self.action_model.id, self.action_model.user_id, self.action_model.request_type,
                       self.company_model.owner_id, self.action_model.status, self.action_model.company_id)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .filter(self.action_model.id == action_id)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def get_action_details(self, action_id: int):
        query = select(self.action_model.id, self.company_model.name, self.user_model.username, self.action_model.status)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .join(self.user_model, self.user_model.id == self.action_model.user_id)\
            .filter(self.action_model.id == action_id)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def update_action(self, action_id, new_status: Status):
        stmt = update(self.action_model).where(self.action_model.id == action_id).values(status=new_status)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_action(self, action_id: int):
        stmt = delete(self.action_model).where(self.action_model.id == action_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_actions(self, user_id, request_type: db_model.ActionType):
        query = select(self.action_model.id, self.company_model.name, self.user_model.username, self.action_model.status)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .join(self.user_model, self.user_model.id == self.action_model.user_id)\
            .filter(self.action_model.request_type == request_type)\
            .filter(self.action_model.user_id == user_id)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def get_company_actions(self, company_id: int, request_type: db_model.ActionType):
        query = select(self.action_model.id, self.company_model.name, self.user_model.username,self.action_model.status)\
            .join(self.company_model, self.action_model.company_id == self.company_model.id)\
            .join(self.user_model, self.user_model.id == self.action_model.user_id)\
            .filter(self.action_model.request_type == request_type)\
            .filter(self.action_model.company_id == company_id)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def add_member(self, company_id: int, user_id: int, role_id: int = 3) -> None:
        new_member = self.member_model(company_id=company_id, user_id=user_id, role_id=role_id)
        self.session.add(new_member)
        await self.session.commit()

    async def get_member_by_user_id(self, user_id: int, company_id: int):
        query = select(self.member_model).filter(self.member_model.user_id == user_id)\
            .filter(self.member_model.company_id == company_id)
        query_result = await self.session.execute(query)
        return query_result.scalar()

    async def get_all_members(self, company_id: int):
        query = select(self.member_model.company_id, self.member_model.user_id,
                       self.user_model.username, self.role_model.role_name).join(self.user_model).join(self.role_model)\
                    .filter(self.member_model.company_id == company_id)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def get_all_admins(self, company_id: int):
        query = select(self.member_model.company_id, self.member_model.user_id,
                       self.user_model.username, self.role_model.role_name).join(self.user_model).join(self.role_model)\
                    .filter(self.member_model.company_id == company_id)\
                    .filter(self.role_model.role_name == RoleName.ADMIN)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def update_member(self, company_id: int, user_id: int, role_id: int = 3) -> None:
        stmt = update(self.member_model).where(self.member_model.company_id == company_id)\
            .where(self.member_model.user_id == user_id).values(role_id=role_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_member(self, user_id: int, company_id: int):
        stmt = delete(self.member_model).where(self.member_model.user_id == user_id)\
            .where(self.member_model.company_id == company_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_role_by_rolename(self, role_name: RoleName):
        query = select(self.role_model).where(role_name == self.role_model.role_name)
        query_result = await self.session.execute(query)
        return query_result.scalar()
