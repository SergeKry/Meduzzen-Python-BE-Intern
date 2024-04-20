import bcrypt


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt


async def decrypt_password(password, salt):
    hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_input_password
