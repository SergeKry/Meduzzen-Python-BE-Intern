from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.utils.utils import create_access_token, validate_password, decode_access_token
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.repository.users import UserRepository
from app.schemas import users as users_schema

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
        user = users_schema.User.from_orm(db_user)
        token = create_access_token(user)
        return token

    @staticmethod
    async def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
        try:
            payload = decode_access_token(token.credentials)
            username = payload.get('username')
            email = payload.get('email')
            user_id = payload.get('sub')
            if not username or not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
            if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')
            return users_schema.User(id=user_id, email=email, username=username)
        except JWTError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err))
