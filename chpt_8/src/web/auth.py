from typing import Annotated

from data.db import Session, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User
from pydantic import BaseModel
from service import auth as service

Db = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(prefix='/auth', tags=['auth'])

class Token(BaseModel):
	access_token: str
	token_type: str = 'bearer'

def unauthorized(detail: str) -> HTTPException:
	return HTTPException(
                     status_code=status.HTTP_401_UNAUTHORIZED,
                     detail=detail,
                     headers={'WWW-Authenticate': 'Bearer'}
                     )

def get_current_user(token: Annotated[str, 
                 Depends(oauth2_scheme)], conn: Db
                 ) -> User:
	user = service.get_current_user(conn, token)
	if user is None:
		raise unauthorized('Could not validate credentials')
	return User(**user.model_dump(exclude={'hash'}))

def get_current_active_user(user: Annotated[User,
                            Depends(get_current_user)],
                            ) -> User:
	if user.disabled:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
		                    detail='Inactive user')
	return user

CurrentUser = Annotated[User, Depends(get_current_active_user)]

def require_role(*roles: str):
	# Dependency factory for role-based access control.
	def checker(user: CurrentUser) -> User:
		if user.role not in roles:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
			                    detail='Not enough permissions')
		return user
	return checker

@router.post('/token')
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], conn: Db) -> Token:
	user = service.auth_user(conn, form.username, form.password)
	if user is None:
		raise unauthorized('Incorrect username or password')
	return Token(access_token=service.create_access_token(user.name))

@router.get('/me')
def me(user: CurrentUser) -> User:
	return user
