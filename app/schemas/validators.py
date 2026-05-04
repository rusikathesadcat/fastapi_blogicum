import re
from datetime import datetime
from typing import Any
from pydantic import field_validator, ValidationInfo
from pydantic_core import PydanticCustomError


def validate_slug(value: str) -> str:
    if not re.match(r'^[a-z0-9-]+$', value):
        raise PydanticCustomError(
            'slug_format',
            'Slug must contain only lowercase letters, numbers and hyphens'
        )
    if len(value) < 2 or len(value) > 50:
        raise PydanticCustomError(
            'slug_length',
            'Slug must be between 2 and 50 characters'
        )
    return value


def validate_username(value: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise PydanticCustomError(
            'username_format',
            'Username must contain only letters, numbers and underscores'
        )
    if len(value) < 3 or len(value) > 150:
        raise PydanticCustomError(
            'username_length',
            'Username must be between 3 and 150 characters'
        )
    return value


def validate_title(value: str) -> str:
    if not value.strip():
        raise PydanticCustomError(
            'title_empty',
            'Title cannot be empty'
        )
    if len(value) > 256:
        raise PydanticCustomError(
            'title_length',
            'Title must not exceed 256 characters'
        )
    return value.strip()


def validate_text(value: str) -> str:
    if not value.strip():
        raise PydanticCustomError(
            'text_empty',
            'Text cannot be empty'
        )
    return value.strip()


def validate_pub_date(value: datetime, info: ValidationInfo) -> datetime:
    if value > datetime.utcnow():
        raise PydanticCustomError(
            'pub_date_future',
            'Publication date cannot be in the future'
        )
    return value


def validate_location_name(value: str) -> str:
    if not value.strip():
        raise PydanticCustomError(
            'name_empty',
            'Location name cannot be empty'
        )
    if len(value) > 256:
        raise PydanticCustomError(
            'name_length',
            'Location name must not exceed 256 characters'
        )
    return value.strip()


def validate_comment_text(value: str) -> str:
    if not value.strip():
        raise PydanticCustomError(
            'comment_empty',
            'Comment text cannot be empty'
        )
    if len(value) > 10000:
        raise PydanticCustomError(
            'comment_length',
            'Comment must not exceed 10000 characters'
        )
    return value.strip()