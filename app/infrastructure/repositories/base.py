from typing import Generic, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from app.database import Base
from app.core.exceptions import DatabaseError

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def _handle_db_error(self, error: Exception, operation: str, context: Optional[dict] = None) -> DatabaseError:
        if isinstance(error, IntegrityError):
            return DatabaseError(
                message=f"Integrity error during {operation}",
                original_error=error,
                context={**context, "error_type": "integrity"} if context else {"error_type": "integrity"}
            )
        if isinstance(error, OperationalError):
            return DatabaseError(
                message=f"Database connection error during {operation}",
                original_error=error,
                context={**context, "error_type": "operational"} if context else {"error_type": "operational"}
            )
        return DatabaseError(
            message=f"Database error during {operation}",
            original_error=error,
            context={**context, "error_type": "generic"} if context else {"error_type": "generic"}
        )

    def get(self, id: int) -> Optional[ModelType]:
        try:
            return self.db_session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise self._handle_db_error(e, "get", {"id": id})

    def get_all(self, skip: int = 0, limit: int = 20) -> list[ModelType]:
        try:
            return self.db_session.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise self._handle_db_error(e, "get_all", {"skip": skip, "limit": limit})

    def create(self, obj_create: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_create)
            self.db_session.add(db_obj)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise self._handle_db_error(e, "create", {"data": obj_create})

    def update(self, id: int, obj_update: dict) -> Optional[ModelType]:
        try:
            db_obj = self.get(id)
            if not db_obj:
                return None
            for field, value in obj_update.items():
                setattr(db_obj, field, value)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise self._handle_db_error(e, "update", {"id": id, "data": obj_update})

    def delete(self, id: int) -> bool:
        try:
            db_obj = self.get(id)
            if not db_obj:
                return False
            self.db_session.delete(db_obj)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise self._handle_db_error(e, "delete", {"id": id})

    def exists_by_field(self, field: str, value: any) -> bool:
        try:
            return self.db_session.query(self.model).filter(getattr(self.model, field) == value).first() is not None
        except SQLAlchemyError as e:
            raise self._handle_db_error(e, "exists_by_field", {"field": field, "value": value})