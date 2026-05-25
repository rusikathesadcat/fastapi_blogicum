from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CommentCreate, CommentUpdate, CommentOut
from app.domain.use_cases.comment_use_case import CommentUseCase
from app.api.error_handler import handle_domain_exception
from app.core.dependencies import get_current_active_user
from app.models import User

router = APIRouter(prefix="/comments", tags=["Comments"])

def get_comment_use_case(db: Session = Depends(get_db)) -> CommentUseCase:
    return CommentUseCase(db)

@router.get("/", response_model=List[CommentOut], summary="Список комментариев")
def list_comments(skip: int = 0, limit: int = 20, use_case: CommentUseCase = Depends(get_comment_use_case)):
    try:
        return use_case.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise handle_domain_exception(e)

@router.get("/{comment_id}", response_model=CommentOut, summary="Получить комментарий")
def get_comment(comment_id: int, use_case: CommentUseCase = Depends(get_comment_use_case)):
    try:
        return use_case.get_by_id(comment_id)
    except Exception as e:
        raise handle_domain_exception(e)

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED, summary="Создать комментарий")
def create_comment(payload: CommentCreate, use_case: CommentUseCase = Depends(get_comment_use_case), current_user: User = Depends(get_current_active_user)):
    try:
        return use_case.create(payload)
    except Exception as e:
        raise handle_domain_exception(e)

@router.put("/{comment_id}", response_model=CommentOut, summary="Обновить комментарий")
def update_comment(comment_id: int, payload: CommentUpdate, use_case: CommentUseCase = Depends(get_comment_use_case), current_user: User = Depends(get_current_active_user)):
    try:
        return use_case.update(comment_id, payload)
    except Exception as e:
        raise handle_domain_exception(e)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить комментарий")
def delete_comment(comment_id: int, use_case: CommentUseCase = Depends(get_comment_use_case), current_user: User = Depends(get_current_active_user)):
    try:
        use_case.delete(comment_id)
    except Exception as e:
        raise handle_domain_exception(e)