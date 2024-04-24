from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.utils.utils import create_access_token, validate_password, decode_access_token
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.repository.users import UserRepository

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth', scheme_name='JWT')


class AuthService:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def user_authenticate(self, username, password):
        user = await UserRepository(self.session).get_one_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not validate_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        token = create_access_token(user.username, user.email, user.id, timedelta(minutes=30))
        return token

    async def get_current_user(self, token: str = Depends(oauth2_bearer)):
        try:
            payload = decode_access_token(token)
            username: str = payload.get('sub')
            email: str = payload.get('email')
            user_id: int = payload.get('user_id')
            if username is None or email is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
            if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')
            return {'username': username, 'email': email, 'user_id': user_id}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
