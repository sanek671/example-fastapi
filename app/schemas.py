from pydantic import BaseModel, EmailStr, conint, ConfigDict
from datetime import datetime
from typing import Optional, Union


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[Union[str, int]] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore
