from app.db.database import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Quiz(BaseModel):
    __tablename__ = "quiz"

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    frequency = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)

    question = relationship("QuizQuestion", back_populates="quiz")


class QuizQuestion(BaseModel):
    __tablename__ = "quiz_question"

    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question = Column(String(255), nullable=False)
    quiz = relationship("Quiz", back_populates="question")
    answer = relationship("QuizAnswers", back_populates="question")


class QuizAnswers(BaseModel):
    __tablename__ = "quiz_answers"

    question_id = Column(Integer, ForeignKey('quiz_question.id', ondelete='CASCADE'), nullable=False)
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    question = relationship("QuizQuestion", back_populates="answer")