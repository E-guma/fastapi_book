from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from config import JWT_SECRET
from data import user as data
from data.error import Missing
from jwt.exceptions import InvalidTokenError
from model.user import UserInDB
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

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


def lookup_user(session: Session, user_id: UUID) -> UserInDB | None:
    # Convert a missing user from the data layer into None.
    try:
        return data.get_one(session, user_id)
    except Missing:
        return None


def auth_user(session: Session, name: str, plain: str) -> UserInDB | None:
    # Authenticate a username and password; return None on any failure.
    user = data.get_by_username(session, name)
    if user is None:
        verify_password(plain, DUMMY_HASH)  # Equal work for unknown users.
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(
    subject: UUID | str, expires: timedelta | None = None
) -> str:
    # Encode a signed access token for the given user id.
    now = datetime.now(UTC)
    lifetime = expires or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        "sub": str(subject),
        "iat": now,
        "exp": now + lifetime,
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    return jwt.encode(claims, JWT_SECRET, algorithm=ALGORITHM)


def get_jwt_user_id(token: str) -> UUID | None:
    # Return the user id from a valid token, or None if validation fails.
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "sub"]},  # Required claims.
        )
    except InvalidTokenError:
        return None
    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub:
        return None
    try:
        return UUID(sub)
    except ValueError:
        # Tokens issued before the UUID change have a username as subject.
        return None


def get_current_user(session: Session, token: str) -> UserInDB | None:
    # Resolve the current user from the token subject.
    user_id = get_jwt_user_id(token)
    if user_id is None:
        return None
    return lookup_user(session, user_id)
