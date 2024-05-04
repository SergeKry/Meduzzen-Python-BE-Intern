from typing import List

from fastapi import HTTPException
from starlette import status
from app.schemas import quiz as quiz_schema
from app.repository.actions import ActionsRepository
from app.db.company import RoleName
from app.repository.quiz import QuizRepository


class QuizService:
    MASTER_ROLES = (RoleName.OWNER, RoleName.ADMIN)

    def __init__(self, user, session):
        self.user = user
        self.session = session
        self.user_role = None
        self.action_repo = ActionsRepository(session)
        self.quiz_repo = QuizRepository(session)

    async def set_user_role(self, company_id: int) -> None:
        member = await self.action_repo.get_member_by_user_id(self.user.id, company_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found')
        self.user_role = member.role_name

    async def get_quiz_details(self, quiz_id: int) -> List[dict]:
        """We don't have public endpoint for this method. Using it to return full quiz details after quiz is created"""
        quiz_details = []
        quiz_questions = await self.quiz_repo.get_quiz_questions(quiz_id)
        for question in quiz_questions:
            correct_answer = await self.quiz_repo.get_quiz_answers(question.id)
            wrong_answer = await self.quiz_repo.get_quiz_answers(question.id, correct=False)
            question_dict = {'question': question.question,
                             'correct_answer': correct_answer,
                             'wrong_answer': wrong_answer}
            quiz_details.append(question_dict)
        return quiz_details

    async def add_quiz(self, request_body: quiz_schema.QuizAddRequest) -> quiz_schema.QuizDetailResponse:
        company_id = request_body.company_id
        await self.set_user_role(company_id)
        if self.user_role not in self.MASTER_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')
        new_quiz = await self.quiz_repo.create_quiz(request_body)
        quiz_details = await self.get_quiz_details(new_quiz.id)
        return quiz_schema.QuizDetailResponse(quiz_id=new_quiz.id, name=new_quiz.name, description=new_quiz.description,
                                              frequency=new_quiz.frequency, questions=quiz_details)

    async def get_all_quizzes(self, company_id: int) -> List[quiz_schema.QuizResponse]:
        await self.set_user_role(company_id)
        result = await self.quiz_repo.get_all_quizzes(company_id)
        quiz_list = [quiz_schema.QuizResponse(id=quiz.id,
                                              name=quiz.name,
                                              description=quiz.description,
                                              frequency=quiz.frequency) for quiz in result]
        return quiz_list

    async def update_quiz(self, quiz_id: int, quiz_data: quiz_schema.QuizUpdateRequest):
        #  we should probably update quiz separately and quiz answers also. We can just upload list of new questions and replace old list
        #  need to check if pydantic schema works in this case.
        pass

    async def delete_quiz(self, quiz_id: int) -> None:
        quiz = await self.quiz_repo.get_quiz(quiz_id)
        await self.set_user_role(quiz.company_id)
        if self.user_role not in self.MASTER_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')
        await self.quiz_repo.delete_quiz(quiz_id)
