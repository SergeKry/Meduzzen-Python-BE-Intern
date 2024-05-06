from typing import List
from pydantic import BaseModel, Field, conlist


class AnswerDetails(BaseModel):
    answer_id: int
    answer: str
    is_correct: bool


class Question(BaseModel):
    question: str = Field(max_length=255)
    correct_answer: conlist(str)
    wrong_answer: conlist(str)


class QuestionDetailedResponse(BaseModel):
    question_id: int
    question: str
    answers: List[AnswerDetails]


class QuestionAddRequest(BaseModel):
    quiz_id: int = Field(gt=0)
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


class QuizDetailResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    frequency: int = Field(gt=0)
    questions: conlist(QuestionDetailedResponse)


class QuizUpdateRequest(BaseModel):
    name: str = Field(max_length=100, default=None)
    description: str = Field(max_length=255, default=None)
    frequency: int = Field(gt=0, default=None)


class QuizListResponse(BaseModel):
    company_id: int
    quiz_list: List[QuizResponse]


class ConfirmationResponse(BaseModel):
    message: str
