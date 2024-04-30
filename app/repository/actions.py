import app.db.company as db_model
from app.schemas import actions as action_schema
from app.db.company import Status


class ActionsRepository:
    def __init__(self, session):
        self.session = session
        self.model = db_model.Action

    async def create_action(self, action: action_schema.ActionCreateRequest):
        new_action = self.model(**action.dict(), status=Status.PENDING)
        self.session.add(new_action)
        await self.session.commit()
        return new_action
