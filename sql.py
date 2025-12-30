import psycopg2
from psycopg2 import sql
from config import load_config
from connect import connect
import sys
from password_generator import generate_password
from vault_encryptor import encrypt

def create_table(cursor):
    query = '''CREATE TABLE IF NOT EXISTS public.vault
    (URL TEXT PRIMARY KEY     NOT NULL,
    usrname           TEXT    NOT NULL,
    passwd         BYTEA NOT NULL);'''

    cursor.execute(query)

def create_master_table(cursor):
    main_query = '''
    CREATE TABLE IF NOT EXISTS master 
    (id BOOLEAN PRIMARY KEY DEFAULT TRUE CHECK (id),
    username TEXT NOT NULL,
    passwd   BYTEA NOT NULL );
    '''
    revoke_query = '''REVOKE UPDATE, DELETE ON master FROM PUBLIC;'''
    grant_query = '''GRANT SELECT ON master TO postgres;'''

    cursor.execute(main_query)
    cursor.execute(revoke_query)
    cursor.execute(grant_query)

def create_metadata_table(cursor):
    query = '''
    CREATE TABLE IF NOT EXISTS vault_metadata
    (id INTEGER PRIMARY KEY CHECK (id = 1),
    kdf_salt BYTEA NOT NULL);
    '''

    cursor.execute(query)

def insert_entry(cursor, data, master_key, salt, pw=False):
    if not pw:
        pw_len = 20
        if len(data) == 3:
            pw_len = int(data[2])
            print(pw_len)
        pw = generate_password(pw_len)
        pw_encrypted = encrypt(pw, master_key, salt)
        data = data[:2] + [pw_encrypted]
    else:
        data[2] = encrypt(data[2], master_key, salt)
    query = '''INSERT INTO vault (URL, usrname, passwd) VALUES (%s, %s, %s)'''
    cursor.execute(query, data)

def insert_master_table(cursor, data):
    query = '''INSERT INTO master (username, passwd) VALUES (%s, %s)'''

    try:
        cursor.execute(query, data)
    except psycopg2.errors.UniqueViolation:
        raise RuntimeError("Master user already exists")
    #add cases: pw lengths too short or long

def insert_metadata_table(cursor, salt):
    query = '''INSERT INTO vault_metadata (id, kdf_salt)
        VALUES (1, %s)
        ON CONFLICT (id) DO NOTHING'''

    cursor.execute(query, (salt,))

def delete_entry(cursor, data):
    query = '''DELETE FROM vault where URL = %s'''
    cursor.execute(query, data)

def update_entry(cursor, data, col, master_key=None, salt=None):
    if len(data)==1:
        pw = generate_password(20)
        pw_encrypted = encrypt(pw, master_key, salt)
        data += [pw_encrypted]
    elif master_key:
        data[0] = encrypt(data[0], master_key, salt)
    query = sql.SQL(
    "UPDATE vault SET {column} = %s WHERE URL = %s"
    ).format(
        column=sql.Identifier(col)
    )
    cursor.execute(query, data)
    #add cases: choose pw length

def print_table(cursor):
    query = '''SELECT * FROM vault'''
    cursor.execute(query)

    rows = cursor.fetchall()
    return rows

def lookup_entry(cursor, data):
    query = '''SELECT * FROM vault WHERE URL = %s'''
    cursor.execute(query, (data,))

    rows = cursor.fetchall()
    return rows

def lookup_master_password(cursor):
    query = '''SELECT passwd FROM master LIMIT 1'''
    cursor.execute(query)

    return cursor.fetchone()

def load_vault_salt(cursor):
    query = '''SELECT kdf_salt FROM vault_metadata WHERE id = 1'''
    cursor.execute(query)

    row = cursor.fetchone()
    if not row:
        raise RuntimeError("Vault not initialized")
    return bytes(row[0])