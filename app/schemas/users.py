from typing import List
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class User(BaseModel):
    id: int
    username: str
    email: str


class SignInRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=127)


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=127)
    password2: str = Field(min_length=8, max_length=127)
    role: int = Field(ge=1, le=3, default=2)

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v


class UserUpdateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(min_length=8, max_length=127, default=None)
    password2: str = Field(min_length=8, max_length=127, default=None)
    role: int = Field(ge=1, le=3, default=None)

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v


class UserDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    role: int


class UserListResponse(BaseModel):
    users: List[UserDetailResponse]


class ConfirmationResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str
