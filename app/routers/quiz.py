from fastapi import APIRouter, HTTPException
from starlette import status
from app.schemas import quiz as quiz_schema


quiz_router = APIRouter(prefix='/quiz', tags=['Quiz'])


@quiz_router.post('/', response_model=quiz_schema.QuizResponse ,status_code=status.HTTP_201_CREATED)
async def add_quiz(request_body: quiz_schema.QuizAddRequest):
    pass


@quiz_router.patch('/{quiz_id}', response_model=quiz_schema.QuizResponse ,status_code=status.HTTP_200_OK)
async def update_quiz(quiz_id: int, request_body: quiz_schema.QuizUpdateRequest):
    pass


@quiz_router.delete('/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int):
    pass


@quiz_router.get('/', response_model=quiz_schema.QuizListResponse ,status_code=status.HTTP_200_OK)
async def get_all_quizzes(request_body: quiz_schema.QuizListRequest):
    pass