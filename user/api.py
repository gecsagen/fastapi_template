from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .services import get_current_user_from_token
from .services import _create_new_user
from .services import _delete_user
from .services import _get_user_by_id
from .services import _update_user
from .schemas import DeleteUserResponse
from .schemas import ShowUser
from .schemas import UpdatedUserResponse
from .schemas import UpdateUserRequest
from .schemas import UserCreate
from .models import User
from session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


#  создание нового пользователя
@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        #  вызывается функция создания нового пользователя
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


#  удаление пользователя
@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    #  вызывается функция удаления пользователя
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


#  получение пользователя по id
@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    #  вызывается функция получения пользователя по id
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


#  обновление пользователя
@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID,
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    #  проверка переданы ли какие-то параметры для изменения пользователя
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    #  вызывается функция получения пользователя по id и затем проверка наличия пользователя
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        #  вызывается функция обновления пользователя
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
