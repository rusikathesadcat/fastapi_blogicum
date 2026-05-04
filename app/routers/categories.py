from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut
from app.domain.use_cases.category_use_case import CategoryUseCase
from app.api.error_handler import handle_domain_exception

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_use_case(db: Session = Depends(get_db)) -> CategoryUseCase:
    return CategoryUseCase(db)


@router.get("/", response_model=List[CategoryOut], summary="Список категорий")
def list_categories(skip: int = 0, limit: int = 20, use_case: CategoryUseCase = Depends(get_category_use_case)):
    try:
        return use_case.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise handle_domain_exception(e)


@router.get("/{category_id}", response_model=CategoryOut, summary="Получить категорию")
def get_category(category_id: int, use_case: CategoryUseCase = Depends(get_category_use_case)):
    try:
        return use_case.get_by_id(category_id)
    except Exception as e:
        raise handle_domain_exception(e)


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED, summary="Создать категорию")
def create_category(payload: CategoryCreate, use_case: CategoryUseCase = Depends(get_category_use_case)):
    try:
        return use_case.create(payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.put("/{category_id}", response_model=CategoryOut, summary="Обновить категорию")
def update_category(category_id: int, payload: CategoryUpdate, use_case: CategoryUseCase = Depends(get_category_use_case)):
    try:
        return use_case.update(category_id, payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить категорию")
def delete_category(category_id: int, use_case: CategoryUseCase = Depends(get_category_use_case)):
    try:
        use_case.delete(category_id)
    except Exception as e:
        raise handle_domain_exception(e)