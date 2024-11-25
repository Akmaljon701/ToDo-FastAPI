from app.auth import get_password_hash, create_access_token
from app.tasks.models import Task
from app.base.exceptions import exception, ErrorCodes, success
from app.base.paginations import Pagination


class TaskService:

    @staticmethod
    async def create(form, db, user):
        task = Task(
            title=form.title,
            body=form.body,
            user_id=user.id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return success(201)

    @staticmethod
    async def get_tasks(db, user, page, limit):
        tasks = db.query(Task).filter_by(user_id=user.id)
        return Pagination(tasks, page, limit).get_paginated_response()

    @staticmethod
    async def get_task(task_id, db, user):
        task = db.query(Task).filter_by(id=task_id, user_id=user.id).first()
        if not task:
            raise exception(ErrorCodes.TASK_NOT_FOUND)
        return task

    @staticmethod
    async def update(task_id, form, db, user):
        task = db.query(Task).filter_by(id=task_id, user=user.id).first()

        if not task:
            raise exception(ErrorCodes.TASK_NOT_FOUND)

        task.title = form.title
        task.body = form.body
        task.execution_datetime = form.execution_datetime

        db.commit()
        db.refresh(task)

        raise success(200)