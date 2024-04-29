from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.services.users import UserService
from app.utils.utils import create_access_token, validate_password, decode_access_token
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.repository.users import UserRepository
from app.schemas import users as user_schema
from app.db.database import get_session

token_auth_scheme = HTTPBearer()


class AuthService:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def user_authenticate(self, username, password):
        db_user = await UserRepository(self.session).get_one_by_username(username)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not validate_password(password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        user = user_schema.User.from_orm(db_user)
        token = create_access_token(user)
        return token

    @staticmethod
    async def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
                               session: AsyncSession = Depends(get_session)) -> user_schema.User:
        try:
            user_id, email, username = decode_access_token(token.credentials)
            user = await UserRepository(session).get_one_by_email(email)
            if not user:
                new_payload_user = user_schema.User(id=user_id, email=email, username=username)
                user = await UserService(session).create_user_from_auth0(new_payload_user)
            return user_schema.User.from_orm(user)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')
