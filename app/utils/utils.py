import bcrypt


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    string_hashed = hashed_password.decode('utf-8')
    return string_hashed


def check_password(password, hashed):
    hashed_input_password = bcrypt.checkpw(password.encode('utf-8'), hashed)
    return hashed_input_password
