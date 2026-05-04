from typing import Any, Optional


class AppException(Exception):
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(AppException):
    def __init__(self, message: str, original_error: Optional[Exception] = None, context: Optional[dict[str, Any]] = None):
        details = {"original_error": str(original_error), **(context or {})}
        super().__init__(message, details)
        self.original_error = original_error


class NotFoundError(AppException):
    def __init__(self, entity: str, entity_id: Any, context: Optional[dict[str, Any]] = None):
        message = f"{entity} with id {entity_id} not found"
        details = {"entity": entity, "entity_id": entity_id, **(context or {})}
        super().__init__(message, details)
        self.entity = entity
        self.entity_id = entity_id


class ValidationError(AppException):
    def __init__(self, field: str, value: Any, message: str, context: Optional[dict[str, Any]] = None):
        details = {"field": field, "value": value, **(context or {})}
        super().__init__(message, details)
        self.field = field
        self.value = value


class ConflictError(AppException):
    def __init__(self, entity: str, field: str, value: Any, context: Optional[dict[str, Any]] = None):
        message = f"{entity} with {field}='{value}' already exists"
        details = {"entity": entity, "field": field, "value": value, **(context or {})}
        super().__init__(message, details)
        self.entity = entity
        self.field = field
        self.value = value