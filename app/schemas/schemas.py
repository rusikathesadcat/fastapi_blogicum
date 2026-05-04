from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo
from app.schemas.validators import (
    validate_slug, validate_username, validate_title,
    validate_text, validate_pub_date, validate_location_name,
    validate_comment_text
)

Slug = Annotated[str, field_validator('slug')(validate_slug)]
Username = Annotated[str, field_validator('username')(validate_username)]
Title = Annotated[str, field_validator('title')(validate_title)]
Text = Annotated[str, field_validator('text')(validate_text)]
LocationName = Annotated[str, field_validator('name')(validate_location_name)]
CommentText = Annotated[str, field_validator('text')(validate_comment_text)]


class UserBase(BaseModel):
    username: Username
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    bio: str = ""


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('email')
    @classmethod
    def validate_email_update(cls, v: Optional[EmailStr], info: ValidationInfo) -> Optional[EmailStr]:
        if v is not None and not v:
            raise ValueError('Email cannot be empty')
        return v


class UserOut(UserBase):
    id: int
    is_active: bool
    date_joined: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    title: Title
    description: str
    slug: Slug
    is_published: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[Title] = None
    description: Optional[str] = None
    slug: Optional[Slug] = None
    is_published: Optional[bool] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LocationBase(BaseModel):
    name: LocationName
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[LocationName] = None
    is_published: Optional[bool] = None


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: Title
    text: Text
    pub_date: datetime
    is_published: bool = True
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None

    @field_validator('pub_date')
    @classmethod
    def validate_pub_date_field(cls, v: datetime, info: ValidationInfo) -> datetime:
        return validate_pub_date(v, info)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[Title] = None
    text: Optional[Text] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None

    @field_validator('pub_date')
    @classmethod
    def validate_pub_date_update(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        if v is not None:
            return validate_pub_date(v, info)
        return v


class PostOut(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostDetail(PostOut):
    author: UserOut
    category: Optional[CategoryOut] = None
    location: Optional[LocationOut] = None
    comments: List["CommentOut"] = []

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    text: CommentText
    post_id: int
    author_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[CommentText] = None


class CommentOut(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


PostDetail.model_rebuild()