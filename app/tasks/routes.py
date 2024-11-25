from itertools import takewhile
from typing import List

from fastapi import APIRouter, Query

from app.auth import SessionDep, CurrentUser

from app.tasks import views
from app.tasks.schemas import responses, schemas
from app.base.exceptions import ErrorResponse, SuccessResponse
from app.base.paginations import PaginatedResponse

task_router = APIRouter(
    tags=['Tasks section'],
    prefix='/tasks'
)

@task_router.post(
    "/create",
    response_model=SuccessResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def create_user(
        form: schemas.TaskCreate,
        db: SessionDep,
        user: CurrentUser
):
    return await views.TaskService.create(form, db, user)

@task_router.get(
    '/',
    response_model=PaginatedResponse[schemas.Tasks],
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_tasks(
        db: SessionDep,
        user: CurrentUser,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
):
    return await views.TaskService.get_tasks(db, user, page, limit)

@task_router.get(
    '/{task_id}',
    response_model=schemas.Task,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def get_task(
        task_id: int,
        db: SessionDep,
        user: CurrentUser,
):
    return await views.TaskService.get_task(task_id, db, user)

@task_router.put(
    "/update/{task_id}",
    response_model=SuccessResponse,
    status_code=200,
    responses={
        400: {"model": ErrorResponse},
    }
)
async def update_task(
        task_id: int,
        form: schemas.TaskUpdate,
        db: SessionDep,
        user: CurrentUser,
):
    return await views.TaskService.update(task_id, form, db, user)



