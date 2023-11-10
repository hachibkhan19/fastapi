from typing import Optional
from pydantic import BaseModel


class Blog(BaseModel):
    name: str
    description: str
    published: Optional[bool]


class User(BaseModel):
    name: str
    email: str
    password:str

class ShowUser(BaseModel):
    name: str
    email: str
    
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    name:str
    description:str
    writter: ShowUser
    
    class Config:
        orm_mode = True


class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
