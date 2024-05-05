from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import quiz as quiz_model
from app.schemas import quiz as quiz_schema


class QuizRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.quiz_model = quiz_model.Quiz

    async def create_quiz(self, quiz_details: quiz_schema.QuizAddRequest) -> quiz_model.Quiz:
        quiz_dict = {'name': quiz_details.name, 'description': quiz_details.description,
                     'frequency': quiz_details.frequency, 'company_id': quiz_details.company_id}
        new_quiz = quiz_model.Quiz(**quiz_dict)
        questions = []
        correct_answers = []
        wrong_answers = []
        for item in quiz_details.questions:
            question = (quiz_model.QuizQuestion(question=item.question, quiz=new_quiz))
            questions.append(question)
            correct_answer = quiz_model.QuizAnswers(answer=item.correct_answer[0], is_correct=True, question=question)
            correct_answers.append(correct_answer)
            wrong_answer_list = [quiz_model.QuizAnswers(answer=answer, is_correct=False,
                                                        question=question) for answer in item.wrong_answer]
            for answer in wrong_answer_list:
                wrong_answers.append(answer)
        self.session.add(new_quiz)
        self.session.add_all(questions)
        self.session.add_all(correct_answers)
        self.session.add_all(wrong_answers)
        await self.session.commit()
        return new_quiz

    async def get_quiz(self, quiz_id):
        query = select(quiz_model.Quiz).where(quiz_model.Quiz.id == quiz_id)
        query_result = await self.session.execute(query)
        return query_result.scalar()

    async def get_quiz_questions(self, quiz_id):
        query = select(quiz_model.QuizQuestion).where(quiz_model.QuizQuestion.quiz_id == quiz_id)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def get_quiz_answers(self, question_id: int):
        query = select(quiz_model.QuizAnswers.id, quiz_model.QuizAnswers.answer, quiz_model.QuizAnswers.is_correct)\
            .filter(quiz_model.QuizAnswers.question_id == question_id)
        query_result = await self.session.execute(query)
        return query_result.all()

    async def get_all_quizzes(self, company_id: int):
        query = select(quiz_model.Quiz).where(quiz_model.Quiz.company_id == company_id)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def update_quiz(self, quiz_id: int, quiz_details: dict):
        stmt = update(quiz_model.Quiz).where(quiz_model.Quiz.id == quiz_id).values(**quiz_details)
        await self.session.execute(stmt)
        await self.session.commit()

    async def add_question(self, question_details: quiz_schema.QuestionAddRequest):
        question = quiz_model.QuizQuestion(quiz_id=question_details.quiz_id, question=question_details.question)
        correct_answer = quiz_model.QuizAnswers(answer=question_details.correct_answer[0],
                                                is_correct=True, question=question)
        wrong_answers = [quiz_model.QuizAnswers(answer=answer, is_correct=False,
                                                question=question) for answer in question_details.wrong_answer]
        self.session.add(question)
        self.session.add(correct_answer)
        self.session.add_all(wrong_answers)
        await self.session.commit()

    async def get_question_by_id(self, question_id):
        query = select(quiz_model.QuizQuestion, quiz_model.Quiz).join(quiz_model.Quiz).where(quiz_model.QuizQuestion.id == question_id)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def delete_question(self, question_id):
        stmt = delete(quiz_model.QuizQuestion).where(quiz_model.QuizQuestion.id == question_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_quiz(self, quiz_id: int):
        stmt = delete(self.quiz_model).where(self.quiz_model.id == quiz_id)
        await self.session.execute(stmt)
        await self.session.commit()