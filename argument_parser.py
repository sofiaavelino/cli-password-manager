import argparse
from config import load_config
from sql import *
from connect import connect
from password_generator import generate_password
from vault_encryptor import decrypt

def argument_parser():
    #config = load_config()
    #conn = connect(config)
    #cursor = conn.cursor()

    parser = argparse.ArgumentParser()

    # Add the arguments to the parser
    parser.add_argument(
        "-a", "--add", 
        required=False, 
        nargs='+',
        help="Add entry: URL USERNAME [PASSWORD_LENGTH]"
    )
    
    parser.add_argument(
        "-ap", "--addpassword", 
        required=False, 
        nargs=3,
        metavar=("URL", "USERNAME", "PASSWORD"),
        help="Add entry with specified password"
    )

    parser.add_argument(
        "-uurl", "--updateurl", 
        required=False,
        nargs=2,
        metavar=("NEW_URL", "OLD_URL"),
        help="Update URL"
    )

    parser.add_argument(
        "-uuser", "--updateuser", 
        required=False,
        nargs=2,
        metavar=("NEW_USER", "URL"),
        help="Update username"
    )

    parser.add_argument(
        "-upw", "--updatepassword", 
        required=False,
        nargs='+',
        help="Update password: [NEW_PASSWORD] URL"
    )
    
    parser.add_argument(
        "-d", "--delete", 
        required=False,
        nargs=1,
        metavar=("URL"),
        help="Delete entry by URL"
    )

    parser.add_argument(
        "-l", "--lookup", 
        nargs=1,
        metavar=("URL"),
        required=False,
        help="Lookup entry by URL"
    )

    parser.add_argument(
        "-li", "--list", 
        action="store_true",
        help="List all entries"
    )

    args = vars(parser.parse_args())

    return args

def arg_actions(cursor, args, master_key):

    salt = load_vault_salt(cursor)

    if args['add']:
        insert_entry(cursor, args['add'], master_key, salt)

    if args['addpassword']:
        insert_entry(cursor, args['addpassword'], master_key, salt, True)

    if args['updateurl']:
        update_entry(cursor, args['updateurl'], "url")

    if args['updateuser']:
        update_entry(cursor, args['updateuser'], "usrname")

    if args['updatepassword']:
        update_entry(cursor, args['updatepassword'], "passwd", master_key, salt)

    if args['delete']:
        delete_entry(cursor, args['delete'])

    if args['lookup']:
        rows = lookup_entry(cursor, args['lookup'][0])
        if len(rows) == 0:
            print('No matches found for this URL.')
        for row in rows:
            url, username, password = row
            print(f"URL: {url}")
            print(f"username: {username}")
            print(f"password: {decrypt(password.tobytes(),master_key, salt)}")
            #if len(rows) > 1: print("-" * 65)  # separator line

    if args['list']:
        rows = print_table(cursor)
        for row in rows:
            url, username, password = row
            print(f"URL: {url}")
            print(f"username: {username}")
            print(f"password: {decrypt(password.tobytes(), master_key, salt)}")
            print("-" * 65)  # separator line

    #conn.commit()

#argument_parser()
