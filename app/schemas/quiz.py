from typing import List
from pydantic import BaseModel, Field, conlist


class Question(BaseModel):
    question: str = Field(max_length=255)
    correct_answer: conlist(str, max_length=1)
    wrong_answer: conlist(str)


class QuizAddRequest(BaseModel):
    company_id: int = Field(gt=0)
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    frequency: int = Field(gt=0)
    questions: conlist(Question, min_length=2)


class QuizResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    frequency: int = Field(gt=0)


class QuizDetailResponse(QuizResponse):
    quiz_id: int
    questions: conlist(Question)


class QuizUpdateRequest(QuizResponse):
    questions: conlist(Question)


class QuizListRequest(BaseModel):
    company_id: int = Field(gt=0)


class QuizListResponse(BaseModel):
    company_id: int
    quiz_list: List[QuizResponse]

