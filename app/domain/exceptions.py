from typing import Any, Optional
from app.core.exceptions import AppException


class DomainException(AppException):
    pass


class CategoryNotFoundError(DomainException):
    def __init__(self, category_id: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"Category with id {category_id} not found",
            details={"entity": "Category", "entity_id": category_id, **(context or {})}
        )
        self.category_id = category_id


class CategoryConflictError(DomainException):
    def __init__(self, slug: str, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"Category with slug '{slug}' already exists",
            details={"entity": "Category", "field": "slug", "value": slug, **(context or {})}
        )
        self.slug = slug


class LocationNotFoundError(DomainException):
    def __init__(self, location_id: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"Location with id {location_id} not found",
            details={"entity": "Location", "entity_id": location_id, **(context or {})}
        )
        self.location_id = location_id


class PostNotFoundError(DomainException):
    def __init__(self, post_id: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"Post with id {post_id} not found",
            details={"entity": "Post", "entity_id": post_id, **(context or {})}
        )
        self.post_id = post_id


class CommentNotFoundError(DomainException):
    def __init__(self, comment_id: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"Comment with id {comment_id} not found",
            details={"entity": "Comment", "entity_id": comment_id, **(context or {})}
        )
        self.comment_id = comment_id


class UserNotFoundError(DomainException):
    def __init__(self, user_id: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"User with id {user_id} not found",
            details={"entity": "User", "entity_id": user_id, **(context or {})}
        )
        self.user_id = user_id


class UserConflictError(DomainException):
    def __init__(self, field: str, value: Any, context: Optional[dict[str, Any]] = None):
        super().__init__(
            message=f"User with {field}='{value}' already exists",
            details={"entity": "User", "field": field, "value": value, **(context or {})}
        )
        self.field = field
        self.value = value