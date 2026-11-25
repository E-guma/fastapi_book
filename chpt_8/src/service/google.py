"""Google OpenID Connect client configuration."""
import hashlib
import secrets

import data.user as data
from authlib.integrations.starlette_client import OAuth
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from model.user import GoogleUserInfo, UserInDB
from sqlalchemy.orm import Session

from service.auth import get_hash

REDIRECT_URI = GOOGLE_REDIRECT_URI

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile",
                   "code_challenge_method": "S256"},
)

def _google_name(sub: str) -> str:
    """Derive a unique, <=64-char username from Google's stable sub."""
    prefix = 'google_'
    if len(prefix) + len(sub) <= 64:
        return prefix + sub
    return prefix + hashlib.sha256(sub.encode()).hexdigest()[:32]


def _unusable_hash() -> str:
    """A valid Argon2 hash of a secret nobody will ever see."""
    return get_hash(secrets.token_urlsafe(32))


def resolve_google_user(session: Session, info: GoogleUserInfo) -> UserInDB:
    """Find or create the local user for verified Google claims."""
    existing = data.get_by_google_sub(session, info.sub)
    if existing is not None:
        changes = {
            'email': info.email,
            'email_verified': info.email_verified,
            'picture': info.picture,
        }
        if any(getattr(existing, key) != value for key, value in changes.items()):
            existing = data.modify(
                session, existing.name, existing.model_copy(update=changes)
            )
        return existing

    return data.create(
        session,
        UserInDB(
            name=_google_name(info.sub),
            hash=_unusable_hash(),
            role='user',
            disabled=False,
            google_sub=info.sub,
            email=info.email,
            email_verified=info.email_verified,
            picture=info.picture,
        ),
    )
