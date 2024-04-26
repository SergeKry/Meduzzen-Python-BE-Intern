import string
from datetime import datetime, timedelta
import bcrypt
from jose import jwt
import random
from app.config import settings
from app.schemas import users as users_schema


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    string_hashed = hashed_password.decode('utf-8')
    return string_hashed


def validate_password(password, hashed):
    hashed_input_password = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    return hashed_input_password


def create_access_token(user: users_schema.User):
    payload = {'sub': user.username, 'email': user.email, 'user_id': user.id, 'aud': settings.JWT_AUD}
    expired = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRATION)
    payload.update({'exp': expired})
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token):
    decoded = jwt.decode(token, settings.JWT_ACCESS_SECRET, audience=settings.JWT_AUD,
                         algorithms=[settings.JWT_ALGORITHM])
    return decoded


def generate_random_password():
    string_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    hashed_password = encrypt_password(string_pass)
    return hashed_password
