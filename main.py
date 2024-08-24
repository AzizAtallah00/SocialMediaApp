from fastapi import FastAPI
from DataBase import get_db, engine
import Models
from typing import List
from routers import user, post, auth, like
from fastapi.middleware.cors import CORSMiddleware

Models.Base.metadata.create_all(bind=engine) #to create models
app = FastAPI()


origins = ["*"]
app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(like.router)

