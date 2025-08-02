from typing import Tuple
import os
import hashlib
import hmac

from settings import security_settings

def hash_psw(password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(security_settings.PASSWORD_BYTES)
    psw_hash = hashlib.pbkdf2_hmac(security_settings.PASSWORD_ALGORITHM, password.encode() + security_settings.PASSWORD_PEPPER, salt, 10000)
    return salt, psw_hash
    
def is_correct_psw(salt: bytes, psw_hash: str, password: str):
    return hmac.compare_digest(
            psw_hash, 
            hashlib.pbkdf2_hmac(security_settings.PASSWORD_ALGORITHM, password.encode() + security_settings.PASSWORD_PEPPER, salt, 10000)
        )
