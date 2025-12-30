import bcrypt
import os
from getpass import getpass

from config import load_config
from connect import connect
from sql import *

def master_password():
    config = load_config()
    conn = connect(config)
    cursor = conn.cursor()

    master_user = input('Define your vault username:')
    master_pw = getpass('Define your master password:')
    master_pw_dup = getpass('Confirm your password:')
    validate_master_password(master_pw, master_pw_dup)
    salt = bcrypt.gensalt()
    pw = bcrypt.hashpw(master_pw.encode(), salt)

    create_master_table(cursor)
    insert_master_table(cursor, (master_user, pw))

    kdf_salt = os.urandom(16)
    create_metadata_table(cursor)
    insert_metadata_table(cursor, kdf_salt)

    conn.commit()

def validate_master_password(pw, pw_dup, min_len=8, max_len=128):
    if pw != pw_dup:
        raise ValueError(
            f"Passwords don't match"
        )
    if not (min_len <= len(pw) <= max_len):
        raise ValueError(
            f"Password length must be between {min_len} and {max_len}"
        )

def verify_master_password(cursor):
    #config = load_config()
    #conn = connect(config)
    #cursor = conn.cursor()

    pw = lookup_master_password(cursor)[0]
    pw_bytes = pw.tobytes()

    password_prompt = getpass()
    if bcrypt.checkpw(password_prompt.encode(), pw_bytes):
        return password_prompt
    else:
        raise ValueError(
            f"Password Incorrect"
        )

#master_password()
#verify_master_password()

'''def verify_master_password(cursor, candidate_password: str) -> bool:
    stored_hash = lookup_master_password(cursor)[0]
    stored_hash_bytes = stored_hash.tobytes()

    return bcrypt.checkpw(
        candidate_password.encode(),
        stored_hash_bytes
    )'''