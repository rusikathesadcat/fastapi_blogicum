from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserUpdate, UserOut
from app.domain.use_cases.user_use_case import UserUseCase
from app.api.error_handler import handle_domain_exception

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_use_case(db: Session = Depends(get_db)) -> UserUseCase:
    return UserUseCase(db)


@router.get("/", response_model=List[UserOut], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 20, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        return use_case.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise handle_domain_exception(e)


@router.get("/{user_id}", response_model=UserOut, summary="Получить пользователя")
def get_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        return use_case.get_by_id(user_id)
    except Exception as e:
        raise handle_domain_exception(e)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Создать пользователя")
def create_user(payload: UserCreate, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        return use_case.create(payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.put("/{user_id}", response_model=UserOut, summary="Обновить пользователя")
def update_user(user_id: int, payload: UserUpdate, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        return use_case.update(user_id, payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пользователя")
def delete_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        use_case.delete(user_id)
    except Exception as e:
        raise handle_domain_exception(e)