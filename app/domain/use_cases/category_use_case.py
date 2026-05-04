from typing import Optional
from sqlalchemy.orm import Session
from app.domain.exceptions import CategoryNotFoundError, CategoryConflictError
from app.infrastructure.repositories.category_repository import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryUseCase:
    def __init__(self, db_session: Session):
        self.repository = CategoryRepository(db_session)

    def get_all(self, skip: int, limit: int):
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            raise e

    def get_by_id(self, category_id: int):
        try:
            category = self.repository.get(category_id)
            if not category:
                raise CategoryNotFoundError(category_id=category_id)
            return category
        except CategoryNotFoundError:
            raise
        except Exception as e:
            raise e

    def create(self, payload: CategoryCreate):
        try:
            if self.repository.slug_exists(payload.slug):
                raise CategoryConflictError(slug=payload.slug)
            return self.repository.create(payload.model_dump())
        except CategoryConflictError:
            raise
        except Exception as e:
            raise e

    def update(self, category_id: int, payload: CategoryUpdate):
        try:
            existing = self.repository.get(category_id)
            if not existing:
                raise CategoryNotFoundError(category_id=category_id)
            if payload.slug is not None and payload.slug != existing.slug:
                if self.repository.slug_exists(payload.slug):
                    raise CategoryConflictError(slug=payload.slug)
            update_data = payload.model_dump(exclude_unset=True)
            return self.repository.update(category_id, update_data)
        except (CategoryNotFoundError, CategoryConflictError):
            raise
        except Exception as e:
            raise e

    def delete(self, category_id: int):
        try:
            deleted = self.repository.delete(category_id)
            if not deleted:
                raise CategoryNotFoundError(category_id=category_id)
            return True
        except CategoryNotFoundError:
            raise
        except Exception as e:
            raise e