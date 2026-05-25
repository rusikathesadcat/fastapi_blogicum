from sqlalchemy.orm import Session
from app.domain.exceptions import UserNotFoundError, UserConflictError
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserUseCase:
    def __init__(self, db_session: Session):
        self.repository = UserRepository(db_session)

    def get_all(self, skip: int, limit: int):
        try:
            return self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            raise e

    def get_by_id(self, user_id: int):
        try:
            user = self.repository.get(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            return user
        except UserNotFoundError:
            raise
        except Exception as e:
            raise e

    def create(self, payload: UserCreate):
        try:
            if self.repository.username_exists(payload.username):
                raise UserConflictError(field="username", value=payload.username)
            if self.repository.email_exists(payload.email):
                raise UserConflictError(field="email", value=payload.email)
            user_data = payload.model_dump()
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
            return self.repository.create(user_data)
        except UserConflictError:
            raise
        except Exception as e:
            raise e

    def update(self, user_id: int, payload: UserUpdate):
        try:
            existing = self.repository.get(user_id)
            if not existing:
                raise UserNotFoundError(user_id=user_id)
            if payload.username is not None and payload.username != existing.username:
                if self.repository.username_exists(payload.username):
                    raise UserConflictError(field="username", value=payload.username)
            if payload.email is not None and payload.email != existing.email:
                if self.repository.email_exists(payload.email):
                    raise UserConflictError(field="email", value=payload.email)
            update_data = payload.model_dump(exclude_unset=True)
            return self.repository.update(user_id, update_data)
        except (UserNotFoundError, UserConflictError):
            raise
        except Exception as e:
            raise e

    def delete(self, user_id: int):
        try:
            deleted = self.repository.delete(user_id)
            if not deleted:
                raise UserNotFoundError(user_id=user_id)
            return True
        except UserNotFoundError:
            raise
        except Exception as e:
            raise e

    def authenticate(self, username: str, password: str):
        return self.repository.authenticate_user(username, password)