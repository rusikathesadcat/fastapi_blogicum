from sqlalchemy.orm import Session
from app.models import Location
from app.infrastructure.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self, db_session: Session):
        super().__init__(Location, db_session)