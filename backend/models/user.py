from pydantic import EmailStr, BaseModel

from typing import Union

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: str

class UserUpdateRequest(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    created_at: Union[str, None] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str

