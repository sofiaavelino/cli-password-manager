import secrets
import string
def generate_password(length, forbidden=[]):
    characters = string.ascii_letters + string.digits + string.punctuation
    allowed_chars = [c for c in characters if c not in forbidden]
    safe_password = ''.join(secrets.choice(allowed_chars) for i in range(length))
    return safe_password