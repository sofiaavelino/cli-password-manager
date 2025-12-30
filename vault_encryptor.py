from cryptography.fernet import Fernet
import os
import base64
import hashlib

def derive_key(master_pw: str, salt: bytes) -> bytes:
    key = hashlib.scrypt(
        master_pw.encode(),
        salt=salt,
        n=2**14,   # CPU/memory cost
        r=8,
        p=1,
        dklen=32
    )
    return base64.urlsafe_b64encode(key)


def encrypt(pw, master_pw, salt):
    key = derive_key(master_pw, salt)
    f = Fernet(key)
    encrypted = f.encrypt(pw.encode())
    return encrypted

def decrypt(encrypted_pw, master_pw, salt):
    key = derive_key(master_pw, salt)
    f = Fernet(key)
    decrypted_pw = f.decrypt(encrypted_pw).decode()
    return decrypted_pw