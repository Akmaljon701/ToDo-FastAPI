from typing import List

from fastapi import APIRouter, Query

from app.auth import SessionDep, CurrentUser

from app.users import views
from app.users.schemas import responses, schemas
from app.base.exceptions import ErrorResponse, SuccessResponse
from app.base.paginations import PaginatedResponse

user_router = APIRouter(
    tags=['Users section'],
    prefix='/users'
)


@user_router.post(
    "/create",
    response_model=responses.TokenResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def create_user(
        form: schemas.UserCreate,
        db: SessionDep
):
    access_token = await views.UserService.register(form, db)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.put(
    "/update/{user_id}",
    response_model=SuccessResponse,
    status_code=200,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def update_user(
        user_id: int,
        form: schemas.UserUpdate,
        db: SessionDep,
        user: CurrentUser,
):
    return await views.UserService.update(user_id, form, db)


@user_router.get(
    '/current',
    response_model=schemas.UserCurrent,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_user_current(
        user: CurrentUser
):
    return user


@user_router.put(
    "/current/update",
    response_model=SuccessResponse,
    status_code=200,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def update_user_current(
        form: schemas.UserCurrentUpdate,
        db: SessionDep,
        user: CurrentUser,
):
    return await views.UserService.update_current(user, form, db)


@user_router.get(
    '/',
    response_model=PaginatedResponse[schemas.Users],
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_users(
        db: SessionDep,
        user: CurrentUser,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
):
    return await views.UserService.get_users(db, page, limit)

