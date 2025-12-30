import bcrypt
import os
from getpass import getpass

from config import load_config
from connect import connect
from sql import *

def create_master_password(cursor):
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


def validate_master_password(pw, pw_dup, min_len=8, max_len=128):
    if pw != pw_dup:
        raise ValueError(
            f"Passwords don't match"
        )
    if not (min_len <= len(pw) <= max_len):
        raise ValueError(
            f"Password length must be between {min_len} and {max_len}"
        )

def vault_initialized(cursor):
    if not master_table_exists(cursor):
        return False
    return master_exists(cursor)

def verify_master_password(cursor):

    pw = lookup_master_password(cursor)[0]
    pw_bytes = pw.tobytes()

    password_prompt = getpass()
    if bcrypt.checkpw(password_prompt.encode(), pw_bytes):
        return password_prompt
    else:
        raise ValueError(
            f"Password Incorrect"
        )
