from sqlalchemy.orm import Session
from app.domain.exceptions import LocationNotFoundError
from app.infrastructure.repositories.location_repository import LocationRepository
from app.schemas import LocationCreate, LocationUpdate


class LocationUseCase:
    def __init__(self, db_session: Session):
        self.repository = LocationRepository(db_session)

    def get_all(self, skip: int, limit: int):
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            raise e

    def get_by_id(self, location_id: int):
        try:
            location = self.repository.get(location_id)
            if not location:
                raise LocationNotFoundError(location_id=location_id)
            return location
        except LocationNotFoundError:
            raise
        except Exception as e:
            raise e

    def create(self, payload: LocationCreate):
        try:
            return self.repository.create(payload.model_dump())
        except Exception as e:
            raise e

    def update(self, location_id: int, payload: LocationUpdate):
        try:
            existing = self.repository.get(location_id)
            if not existing:
                raise LocationNotFoundError(location_id=location_id)
            update_data = payload.model_dump(exclude_unset=True)
            return self.repository.update(location_id, update_data)
        except LocationNotFoundError:
            raise
        except Exception as e:
            raise e

    def delete(self, location_id: int):
        try:
            deleted = self.repository.delete(location_id)
            if not deleted:
                raise LocationNotFoundError(location_id=location_id)
            return True
        except LocationNotFoundError:
            raise
        except Exception as e:
            raise e