from pydantic import BaseModel
from uuid import UUID
from typing import Union, List
from datetime import datetime

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    favorite_movies: List[str]

class UserResponse(UserCreateRequest):
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    favorite_movies: List[str]

class UserUpdateRequest(BaseModel):
    id: UUID
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    created_at: Union[datetime, None] = None
    favorite_movies: Union[List[str], None] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserWithToken(BaseModel):
    token: str

