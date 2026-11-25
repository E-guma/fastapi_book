"""Google sign-in routes."""
from authlib.integrations.starlette_client import OAuthError
from data.error import Duplicate
from fastapi import APIRouter, HTTPException, Request
from model.user import GoogleUserInfo
from pydantic import ValidationError
from service import auth as auth_service
from service.google import REDIRECT_URI, oauth, resolve_google_user

from web.auth import SessionDep, Token, unauthorized

router = APIRouter(prefix='/auth/google', tags=['auth'])


@router.get('/login')
async def google_login(request: Request):
    """Redirect the browser to Google to start the OIDC flow."""
    return await oauth.google.authorize_redirect(request, REDIRECT_URI, prompt='select_account')


@router.get('/callback')
async def google_callback(request: Request, session: SessionDep) -> Token:
    """Validate Google's response, resolve the user, issue our JWT."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as exc:
        raise unauthorized('Google sign-in failed') from exc

    try:
        info = GoogleUserInfo.model_validate(dict(token['userinfo']))
    except (KeyError, ValidationError) as exc:
        raise unauthorized('Invalid identity information from Google') from exc

    try:
        user = resolve_google_user(session, info)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg) from exc

    if user.disabled:
        raise HTTPException(status_code=403, detail='Inactive user')

    return Token(access_token=auth_service.create_access_token(user.id))
