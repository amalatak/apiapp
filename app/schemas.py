from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    # define post class to validate schema of input data
    title: str
    content: str 
    published: bool = True # optional value with default setting

class CreatePost(PostBase):
    pass # Same as PostBase

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    # must be capitalized
    Post : PostResponse
    votes : int


class UserCreate(BaseModel):
    email: EmailStr # Make sure valid email
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str 
    token_type : str 

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    direction : conint(le=1)  # Votes are 0 or 1

