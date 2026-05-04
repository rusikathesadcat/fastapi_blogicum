from sqlalchemy.orm import Session
from app.models import Category
from app.infrastructure.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db_session: Session):
        super().__init__(Category, db_session)

    def get_by_slug(self, slug: str) -> Category | None:
        try:
            return self.db_session.query(Category).filter(Category.slug == slug).first()
        except Exception as e:
            raise self._handle_db_error(e, "get_by_slug", {"slug": slug})

    def slug_exists(self, slug: str) -> bool:
        return self.exists_by_field("slug", slug)