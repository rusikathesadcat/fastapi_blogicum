from sqlalchemy.orm import Session, joinedload
from app.models import Post
from app.infrastructure.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, db_session: Session):
        super().__init__(Post, db_session)

    def get_with_relations(self, id: int) -> Post | None:
        try:
            return self.db_session.query(Post).options(
                joinedload(Post.author),
                joinedload(Post.category),
                joinedload(Post.location),
                joinedload(Post.comments)
            ).filter(Post.id == id).first()
        except Exception as e:
            raise self._handle_db_error(e, "get_with_relations", {"id": id})