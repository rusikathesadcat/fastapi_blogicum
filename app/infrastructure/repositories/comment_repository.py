from sqlalchemy.orm import Session
from app.models import Comment
from app.infrastructure.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, db_session: Session):
        super().__init__(Comment, db_session)