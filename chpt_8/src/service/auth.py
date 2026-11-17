import os
from datetime import UTC, datetime, timedelta

import jwt
from data import user as data
from data.error import Missing
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from model.user import UserInDB
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
if SECRET_KEY == None:
    raise RuntimeError("Jwt secret key not set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ISSUER = "E-guma_Cryptid_API"
AUDIENCE = "API_Clients"

password_hash = PasswordHash.recommended()

# Dummy hash used to equalize login timing for unknown usernames.
DUMMY_HASH = password_hash.hash("dummy-password-for-timing")


def get_hash(plain: str) -> str:
    # Return the Argon2 hash of a plain-text password.
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    # Compare a plain-text password with a stored Argon2 hash.
    return password_hash.verify(plain, hashed)


def lookup_user(conn: Session, name: str) -> UserInDB | None:
    # Convert a missing user from the data layer into None.
    try:
        return data.get_one(conn, name)
    except Missing:
        return None


def auth_user(conn: Session, name: str, plain: str) -> UserInDB | None:
    # Authenticate a username and password; return None on any failure.
    user = lookup_user(conn, name)
    if user is None:
        verify_password(plain, DUMMY_HASH)  # Perform equivalent work for unknown users.
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(subject: str, expires: timedelta | None = None) -> str:
    # Encode a signed access token for the given subject.
    now = datetime.now(UTC)
    lifetime = expires or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        "sub": subject,
        "iat": now,
        "exp": now + lifetime,
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def get_jwt_username(token: str) -> str | None:
    # Return the subject from a valid token, or None if validation fails.
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "sub"]},  # Required claims.
        )
    except InvalidTokenError:
        return None
    sub = payload.get("sub")
    return sub if isinstance(sub, str) and sub else None


def get_current_user(conn: Session, token: str) -> UserInDB | None:
    # Resolve the current user from the token subject.
    name = get_jwt_username(token)
    if name is None:
        return None
    return lookup_user(conn, name)
