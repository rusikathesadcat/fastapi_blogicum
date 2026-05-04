from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PostCreate, PostUpdate, PostOut, PostDetail
from app.domain.use_cases.post_use_case import PostUseCase
from app.api.error_handler import handle_domain_exception

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_post_use_case(db: Session = Depends(get_db)) -> PostUseCase:
    return PostUseCase(db)


@router.get("/", response_model=List[PostOut], summary="Список публикаций")
def list_posts(skip: int = 0, limit: int = 20, use_case: PostUseCase = Depends(get_post_use_case)):
    try:
        return use_case.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise handle_domain_exception(e)


@router.get("/{post_id}", response_model=PostDetail, summary="Получить публикацию")
def get_post(post_id: int, use_case: PostUseCase = Depends(get_post_use_case)):
    try:
        return use_case.get_by_id(post_id)
    except Exception as e:
        raise handle_domain_exception(e)


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED, summary="Создать публикацию")
def create_post(payload: PostCreate, use_case: PostUseCase = Depends(get_post_use_case)):
    try:
        return use_case.create(payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.put("/{post_id}", response_model=PostOut, summary="Обновить публикацию")
def update_post(post_id: int, payload: PostUpdate, use_case: PostUseCase = Depends(get_post_use_case)):
    try:
        return use_case.update(post_id, payload)
    except Exception as e:
        raise handle_domain_exception(e)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить публикацию")
def delete_post(post_id: int, use_case: PostUseCase = Depends(get_post_use_case)):
    try:
        use_case.delete(post_id)
    except Exception as e:
        raise handle_domain_exception(e)