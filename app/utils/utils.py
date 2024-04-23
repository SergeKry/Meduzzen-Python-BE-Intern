from datetime import datetime, timedelta
import bcrypt
from jose import jwt
from app.config import settings


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    string_hashed = hashed_password.decode('utf-8')
    return string_hashed


def validate_password(password, hashed):
    hashed_input_password = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    return hashed_input_password


def create_access_token(username: str, email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'email': email, 'id': user_id}
    expired = datetime.utcnow() + expires_delta
    encode.update({'exp': expired})
    return jwt.encode(encode, settings.JWT_ACCESS_SECRET, algorithm=settings.JWT_ALGORITHM)
