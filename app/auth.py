from typing import Annotated

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import Session
from starlette import status

from app import config
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.database import get_db
from app.base.exceptions import exception, ErrorCodes
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_router = APIRouter(prefix='', tags=['Auth auth section'],)

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.JWT_EXPIRE

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

SessionDep = Annotated[Session, Depends(get_db)]

def current_user(db: SessionDep, token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise credentials_exception
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(current_user)]

@auth_router.post("/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter_by(username=form_data.username).first()
    if user:
        validate_password = pwd_context.verify(form_data.password, user.password)
        if not validate_password:
            raise exception(ErrorCodes.INCORRECT_PASSWORD)
    else:
        raise exception(ErrorCodes.USER_NOT_FOUND)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
