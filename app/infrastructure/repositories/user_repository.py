from sqlalchemy.orm import Session
from app.models import User
from app.infrastructure.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: Session):
        super().__init__(User, db_session)

    def get_by_username(self, username: str) -> User | None:
        try:
            return self.db_session.query(User).filter(User.username == username).first()
        except Exception as e:
            raise self._handle_db_error(e, "get_by_username", {"username": username})

    def get_by_email(self, email: str) -> User | None:
        try:
            return self.db_session.query(User).filter(User.email == email).first()
        except Exception as e:
            raise self._handle_db_error(e, "get_by_email", {"email": email})

    def username_exists(self, username: str) -> bool:
        return self.exists_by_field("username", username)

    def email_exists(self, email: str) -> bool:
        return self.exists_by_field("email", email)

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_by_username(username)
        if not user:
            return None
        from app.core.security import verify_password
        if not verify_password(password, user.hashed_password):
            return None
        return user