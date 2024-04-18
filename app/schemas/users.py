from typing import List
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(max_length=320)
    password: str = Field(min_length=8, max_length=127)
    password2: str = Field(min_length=8, max_length=127)
    role: int


class UserUpdateRequest(BaseModel):
    username: str
    password: str
    password2: str
    email: str
    role: int


class UserDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    role: int


class UserListResponse(BaseModel):
    users: List[UserDetailResponse]
