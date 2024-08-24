from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

#user schema
class UserRequest (BaseModel):
    email: EmailStr
    password: str
        
class UserResponse (BaseModel):
    id: int
    email:EmailStr
    createdAt : datetime
    class Config:
        orm_mode = True

#post schema
class Post (BaseModel):
    title: str
    content: str
        
class PostResponse (BaseModel):
    id : int
    title: str
    content: str
    createdAt : datetime
    ownerId : int
    owner : UserResponse
    likes : int
    class Config:
        orm_mode = True

class PostWithLikes (BaseModel):
    Post : PostResponse
    likes : int
    class Config:
        orm_mode = True
        
#token schema
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
    
#like schema
class likeRequest(BaseModel) : 
    postId : int
    dis : bool
    
