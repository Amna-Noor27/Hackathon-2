import bcrypt

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Encode password to bytes and handle truncation if needed
    password_bytes = password.encode('utf-8')

    # Bcrypt has a 72-byte limit for passwords, though this is extremely rare in practice
    # For safety, we'll hash the password as is, since typical passwords are much shorter
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.
    """
    if not plain_password or not hashed_password:
        return False

    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except:
        return False