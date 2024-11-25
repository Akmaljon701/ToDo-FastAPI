from app.auth import get_password_hash, create_access_token
from app.users.models import User
from app.base.exceptions import exception, ErrorCodes, success
from app.base.paginations import Pagination


class UserService:

    @staticmethod
    async def register(form, db):
        user = db.query(User).filter(User.username == form.username).first()

        if user:
            raise exception(ErrorCodes.USER_ALREADY_EXIST)

        hashed_password = get_password_hash(form.password)
        user = User(username=form.username, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        access_token = create_access_token({'id': user.id})
        return access_token

    @staticmethod
    async def update(user_id, form, db):
        user = db.query(User).filter_by(id=user_id).first()

        if not user:
            raise exception(ErrorCodes.USER_NOT_FOUND)

        if form.username:
            existing_user = db.query(User).filter(User.id != user_id, User.username == form.username).first()
            if existing_user:
                raise exception(ErrorCodes.USERNAME_ALREADY_EXIST)
            user.username = form.username

        if form.password:
            user.password = get_password_hash(form.password)

        db.commit()
        db.refresh(user)

        raise success(200)

    @staticmethod
    async def update_current(user, form, db):
        if form.username:
            existing_user = db.query(User).filter(User.id != user.id, User.username == form.username).first()
            if existing_user:
                raise exception(ErrorCodes.USERNAME_ALREADY_EXIST)
            user.username = form.username

        if form.password:
            user.password = get_password_hash(form.password)

        db.commit()
        db.refresh(user)

        raise success(200)

    @staticmethod
    async def get_users(db, page, limit):
        users = db.query(User)
        return Pagination(users, page, limit).get_paginated_response()
