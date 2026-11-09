"""
This file handles three important things:
1. Password hashing.
2. JWT generation and verification.
3. Encryption and decryption.
"""

import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash
from cryptography.fernet import Fernet

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


"""
This creates a password hashing configuration using a recommended algorithm and settings supported by pwdlib.
You use this object whenever you need to hash or verify passwords.
"""
password_hash = PasswordHash.recommended()


"""
This initializes your Fernet encryption system.
Unlike password hashing, encryption is reversible.
You need a secret encryption key to encrypt and decrypt your data.
For example, you might want to encrypt users' private notes before storing them in your database.
Fernet requires a valid key generated using its key-generation method.
"""
fernet = Fernet(
    os.getenv("FERNET_KEY").encode()
)


# PASSWORD HASHING
def hash_password(password: str):
    return password_hash.hash(password)


# PASSWORD VERIFICATION
def verify_password(password: str, hashed_password: str):
    return password_hash.verify(
        password,
        hashed_password
    )


#This function creates a JWT access token for a user.
def create_access_token(user_id: int, role: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# REFRESH TOKEN
def create_refresh_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# JWT VERIFICATION
def decode_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )




# ENCRYPTION
def encrypt_content(content: str):

    return fernet.encrypt(
        content.encode()
    ).decode()


# DECRYPTION
def decrypt_content(encrypted_content: str):

    return fernet.decrypt(
        encrypted_content.encode()
    ).decode()



#Passwords → Hashing.
#Notes → Encryption.