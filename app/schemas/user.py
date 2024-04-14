from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str
    role: int


class UserUpdateRequest(BaseModel):
    id: int
    username: str
    password: str
    email: str
    role: int


class UserListResponse(BaseModel):
    users: List[User]


class UserDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    role: int
