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

    async def check_master_permissions(self, company_id: int) -> None:
        await self.set_user_role(company_id)
        if self.user_role not in self.MASTER_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    async def get_quiz_details(self, quiz_id: int) -> List[dict]:
        """We don't have public endpoint for this method. Using it to return full quiz details after quiz is created"""
        quiz_details = []
        quiz_questions = await self.quiz_repo.get_quiz_questions(quiz_id)
        for question in quiz_questions:
            answers = await self.quiz_repo.get_quiz_answers(question.id)
            print(answers)
            answers = [quiz_schema.AnswerDetails(answer_id=answer.id, answer=answer.answer, is_correct=answer.is_correct) for answer in answers]
            question_details = {'question_id': question.id, 'question': question.question, 'answers': answers}
            quiz_details.append(question_details)
        return quiz_details

    async def add_quiz(self, request_body: quiz_schema.QuizAddRequest) -> quiz_schema.QuizDetailResponse:
        company_id = request_body.company_id
        await self.check_master_permissions(company_id)
        new_quiz = await self.quiz_repo.create_quiz(request_body)
        quiz_details = await self.get_quiz_details(new_quiz.id)
        return quiz_schema.QuizDetailResponse(id=new_quiz.id, name=new_quiz.name, description=new_quiz.description,
                                              frequency=new_quiz.frequency, questions=quiz_details)

    async def get_all_quizzes(self, company_id: int) -> List[quiz_schema.QuizResponse]:
        await self.set_user_role(company_id)
        result = await self.quiz_repo.get_all_quizzes(company_id)
        quiz_list = [quiz_schema.QuizResponse(id=quiz.id,
                                              name=quiz.name,
                                              description=quiz.description,
                                              frequency=quiz.frequency) for quiz in result]
        return quiz_list

    async def update_quiz(self, quiz_id, quiz_data: quiz_schema.QuizUpdateRequest):
        quiz = await self.quiz_repo.get_quiz(quiz_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz not found')
        await self.check_master_permissions(quiz.company_id)
        quiz_data_dict = quiz_data.dict(exclude_unset=True)
        await self.quiz_repo.update_quiz(quiz_id, quiz_data_dict)
        updated_quiz = await self.quiz_repo.get_quiz(quiz_id)
        return quiz_schema.QuizResponse(id=updated_quiz.id, name=updated_quiz.name,
                                        description=updated_quiz.description, frequency=updated_quiz.frequency)

    async def delete_quiz(self, quiz_id: int) -> None:
        quiz = await self.quiz_repo.get_quiz(quiz_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz not found')
        await self.check_master_permissions(quiz.company_id)
        await self.quiz_repo.delete_quiz(quiz_id)

    async def add_question(self, question_details: quiz_schema.QuestionAddRequest):
        quiz = await self.quiz_repo.get_quiz(question_details.quiz_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz not found')
        await self.check_master_permissions(quiz.company_id)
        await self.quiz_repo.add_question(question_details)

    async def delete_question(self, question_id):
        question, quiz = await self.quiz_repo.get_question_by_id(question_id)
        await self.check_master_permissions(quiz.company_id)
        await self.quiz_repo.delete_question(question_id)
