from fastapi import APIRouter, HTTPException
from starlette import status
from app.schemas import quiz as quiz_schema
from app.services.quiz import QuizService
from app.routers.routers import db_dependency, user_dependency


quiz_router = APIRouter(prefix='/quiz', tags=['Quizzes'])


@quiz_router.post('/', response_model=quiz_schema.QuizDetailResponse, status_code=status.HTTP_201_CREATED)
async def add_quiz(request_body: quiz_schema.QuizAddRequest, user: user_dependency, session: db_dependency):
    new_quiz = await QuizService(user, session).add_quiz(request_body)
    return new_quiz


@quiz_router.get('/{company_id}', response_model=quiz_schema.QuizListResponse, status_code=status.HTTP_200_OK)
async def get_all_quizzes(company_id: int, user: user_dependency, session: db_dependency):
    quizzes = await QuizService(user, session).get_all_quizzes(company_id)
    return quiz_schema.QuizListResponse(company_id=company_id, quiz_list=quizzes)


@quiz_router.put('/{quiz_id}', response_model=quiz_schema.QuizResponse ,status_code=status.HTTP_200_OK)
async def update_quiz(quiz_id: int, request_body: quiz_schema.QuizUpdateRequest,
                      user: user_dependency, session: db_dependency):
    await QuizService(user, session)


@quiz_router.delete('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int, user: user_dependency, session: db_dependency):
    await QuizService(user, session).delete_quiz(quiz_id)
