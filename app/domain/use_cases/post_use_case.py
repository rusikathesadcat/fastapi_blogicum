from sqlalchemy.orm import Session
from app.domain.exceptions import PostNotFoundError, CategoryNotFoundError, LocationNotFoundError
from app.infrastructure.repositories.post_repository import PostRepository
from app.infrastructure.repositories.category_repository import CategoryRepository
from app.infrastructure.repositories.location_repository import LocationRepository
from app.schemas import PostCreate, PostUpdate


class PostUseCase:
    def __init__(self, db_session: Session):
        self.repository = PostRepository(db_session)
        self.category_repository = CategoryRepository(db_session)
        self.location_repository = LocationRepository(db_session)

    def get_all(self, skip: int, limit: int):
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            raise e

    def get_by_id(self, post_id: int):
        try:
            post = self.repository.get_with_relations(post_id)
            if not post:
                raise PostNotFoundError(post_id=post_id)
            return post
        except PostNotFoundError:
            raise
        except Exception as e:
            raise e

    def create(self, payload: PostCreate):
        try:
            if payload.category_id and not self.category_repository.get(payload.category_id):
                raise CategoryNotFoundError(category_id=payload.category_id)
            if payload.location_id and not self.location_repository.get(payload.location_id):
                raise LocationNotFoundError(location_id=payload.location_id)
            return self.repository.create(payload.model_dump())
        except (CategoryNotFoundError, LocationNotFoundError):
            raise
        except Exception as e:
            raise e

    def update(self, post_id: int, payload: PostUpdate):
        try:
            existing = self.repository.get(post_id)
            if not existing:
                raise PostNotFoundError(post_id=post_id)
            if payload.category_id is not None and payload.category_id != existing.category_id:
                if not self.category_repository.get(payload.category_id):
                    raise CategoryNotFoundError(category_id=payload.category_id)
            if payload.location_id is not None and payload.location_id != existing.location_id:
                if not self.location_repository.get(payload.location_id):
                    raise LocationNotFoundError(location_id=payload.location_id)
            update_data = payload.model_dump(exclude_unset=True)
            return self.repository.update(post_id, update_data)
        except (PostNotFoundError, CategoryNotFoundError, LocationNotFoundError):
            raise
        except Exception as e:
            raise e

    def delete(self, post_id: int):
        try:
            deleted = self.repository.delete(post_id)
            if not deleted:
                raise PostNotFoundError(post_id=post_id)
            return True
        except PostNotFoundError:
            raise
        except Exception as e:
            raise e