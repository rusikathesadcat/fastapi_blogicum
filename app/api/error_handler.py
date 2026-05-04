from fastapi import HTTPException, status
from app.domain.exceptions import (
    CategoryNotFoundError, CategoryConflictError,
    LocationNotFoundError,
    PostNotFoundError,
    CommentNotFoundError,
    UserNotFoundError, UserConflictError
)
from app.core.exceptions import DatabaseError, ValidationError, ConflictError, AppException


def handle_domain_exception(exc: Exception) -> HTTPException:
    if isinstance(exc, CategoryNotFoundError | LocationNotFoundError | PostNotFoundError | CommentNotFoundError | UserNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": exc.message, **exc.details}
        )
    if isinstance(exc, CategoryConflictError | UserConflictError | ConflictError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "conflict", "message": exc.message, **exc.details}
        )
    if isinstance(exc, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "validation", "message": exc.message, "field": exc.field, **exc.details}
        )
    if isinstance(exc, DatabaseError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "database_error", "message": exc.message, **exc.details}
        )
    if isinstance(exc, AppException):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "app_error", "message": exc.message, **exc.details}
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={"error": "internal_error", "message": str(exc)}
    )