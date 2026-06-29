from pydantic import BaseModel

from typing import Union, List

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(UserCreateRequest):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: str
    favorite_movies: List[str]

class UserUpdateRequest(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    created_at: Union[str, None] = None
    favorite_movies: Union[List[str], None] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserWithToken(BaseModel):
    token: str

