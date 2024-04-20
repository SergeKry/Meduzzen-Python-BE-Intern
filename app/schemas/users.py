from typing import List
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    username: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=127)
    password2: str = Field(min_length=8, max_length=127)
    role: int = Field(ge=1, le=3, default=2)


class UserUpdateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(min_length=8, max_length=127, default=None)
    password2: str = Field(min_length=8, max_length=127, default=None)
    role: int = Field(ge=1, le=3, default=None)


class UserDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    role: int


class UserListResponse(BaseModel):
    users: List[UserDetailResponse]


class ConfirmationResponse(BaseModel):
    message: str
