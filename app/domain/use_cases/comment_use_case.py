from sqlalchemy.orm import Session
from app.domain.exceptions import CommentNotFoundError, PostNotFoundError, UserNotFoundError
from app.infrastructure.repositories.comment_repository import CommentRepository
from app.infrastructure.repositories.post_repository import PostRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas import CommentCreate, CommentUpdate


class CommentUseCase:
    def __init__(self, db_session: Session):
        self.repository = CommentRepository(db_session)
        self.post_repository = PostRepository(db_session)
        self.user_repository = UserRepository(db_session)

    def get_all(self, skip: int, limit: int):
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            raise e

    def get_by_id(self, comment_id: int):
        try:
            comment = self.repository.get(comment_id)
            if not comment:
                raise CommentNotFoundError(comment_id=comment_id)
            return comment
        except CommentNotFoundError:
            raise
        except Exception as e:
            raise e

    def create(self, payload: CommentCreate):
        try:
            if not self.post_repository.get(payload.post_id):
                raise PostNotFoundError(post_id=payload.post_id)
            if not self.user_repository.get(payload.author_id):
                raise UserNotFoundError(user_id=payload.author_id)
            return self.repository.create(payload.model_dump())
        except (PostNotFoundError, UserNotFoundError):
            raise
        except Exception as e:
            raise e

    def update(self, comment_id: int, payload: CommentUpdate):
        try:
            existing = self.repository.get(comment_id)
            if not existing:
                raise CommentNotFoundError(comment_id=comment_id)
            update_data = payload.model_dump(exclude_unset=True)
            return self.repository.update(comment_id, update_data)
        except CommentNotFoundError:
            raise
        except Exception as e:
            raise e

    def delete(self, comment_id: int):
        try:
            deleted = self.repository.delete(comment_id)
            if not deleted:
                raise CommentNotFoundError(comment_id=comment_id)
            return True
        except CommentNotFoundError:
            raise
        except Exception as e:
            raise e