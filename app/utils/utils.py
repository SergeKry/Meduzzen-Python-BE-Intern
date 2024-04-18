import re
import bcrypt


def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern, email):
        return True


async def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt


async def decrypt_password(password, salt):
    hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input_password
