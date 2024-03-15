import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Literal, Annotated
from sqlmodel import Session
from sqlmodel import Session, SQLModel, select
from pydantic import ValidationError
from backend.models.entities import (
    UserInDB,
    AccessToken,
    UserRegistration,
    InvalidCredentials,
    InvalidToken,
    ExpiredToken,
    Claims
)
from backend.models.user import User
from backend import database as db

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_key = str(os.environ.get("JWT_KEY", default="any string you want for a dev JWT key"))
jwt_alg = "HS256"

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# ******************************
#			MODELS
# ******************************



# ******************************
#			ROUTES
# ******************************
    
@auth_router.post("/registration",
                  response_model=User,
                  status_code=201)
def register_new_user(
    registration: UserRegistration,
    session: Annotated[Session, Depends(db.get_session)]):
    """Register new user."""
    if db.check_credentials_exist(session, registration.username, registration.email) == False:
            hashed_password = pwd_context.hash(registration.password)
            user = UserInDB(
				**registration.model_dump(),
				hashed_password=hashed_password,
			)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

@auth_router.post("/token", response_model=AccessToken)
def get_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session),
):
    """Get access token for user."""

    user = _get_authenticated_user(session, form)
    return _build_access_token(user)

# ******************************
#			HELPERS
# ******************************

def _get_authenticated_user(
    session: Session,
    form: OAuth2PasswordRequestForm,
) -> UserInDB:
    user = session.exec(
        select(UserInDB).where(UserInDB.username == form.username)
    ).first()

    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()

    return user


def _build_access_token(user: UserInDB) -> AccessToken:
    expiration = int(datetime.now(timezone.utc).timestamp()) + access_token_duration
    claims = Claims(sub=user.id, exp=expiration)
    access_token = jwt.encode(claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )

def get_current_user(
    session: Session = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> UserInDB:
    print("in get current user")
    user = _decode_access_token(session, token)
    return user
    
def _decode_access_token(session: Session, token: str) -> UserInDB:
    try:
        print("key", jwt_key)
        print("alg", jwt_alg)
        print("token", token)
        claims_dict = jwt.decode(token, key=jwt_key, algorithms=jwt_alg)
        print(claims_dict)
        claims = Claims(**claims_dict)
        print(claims)
        user_id = claims.sub
        print(user_id)
        user = session.get(UserInDB, user_id)
        print(user)

        if user is None:
            raise InvalidToken()

        return user
    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        print("jwt error")
        raise InvalidToken()
    except ValidationError():
        raise InvalidToken()