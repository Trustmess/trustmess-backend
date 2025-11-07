from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.argon2 import Argon2Hasher

def hash_password_def(user_password):
    password_hash = PasswordHash.recommended()
    hash = password_hash.hash(user_password)

    result = hash
    return result

def verify_hached_password_def(user_password, hashed_pass_in_db):
    password_hash = PasswordHash.recommended()
    valid = password_hash.verify(user_password, hashed_pass_in_db)
    return valid