import psycopg2
from config import load_config
from sql import *
from connect import connect
from password_generator import generate_password
from argument_parser import *
from master_password import verify_master_password, vault_initialized, create_master_password

def main():
    config = load_config()
    conn = connect(config)
    cursor = conn.cursor()

    create_table(cursor) #Creates table if it doesnt exist

    if not vault_initialized(cursor):
        create_master_password()

    args = argument_parser()
    if any(args.values()):
        master_key = verify_master_password(cursor)
        if master_key:
            arg_actions(cursor, args, master_key)

    conn.commit()

main()
