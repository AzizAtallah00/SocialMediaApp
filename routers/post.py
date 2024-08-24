from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy import func
from DataBase import get_db, engine
import Models, Schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[Schemas.PostWithLikes])
def getPosts (db : Session = Depends(get_db), user_id : int = Depends(oauth2.getCurrentUser),limit : int = 10, offset : int = 0, search : Optional[str] = ""):
    postLikes = db.query(Models.Post, func.count(Models.Like.postId).label("likes")).join(Models.Like,Models.Post.id == Models.Like.postId,isouter=True).group_by(Models.Post.id).filter(Models.Post.content.contains(search)).limit(limit).offset(offset).all()
    
    return postLikes

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=Schemas.PostResponse)
def addPost(post : Schemas.Post, db : Session = Depends(get_db), user : int = Depends(oauth2.getCurrentUser)):
    post1 = Models.Post(ownerId = user.id, title = post.title, content = post.content)
    db.add(post1)
    db.commit()
    db.refresh(post1)
    return post1

@router.get("/mypost",response_model=List[Schemas.PostWithLikes])
def getMyPosts(db : Session = Depends(get_db), currUser : int = Depends(oauth2.getCurrentUser), limit: int=10, offset: int=0, search: Optional[str]=""):
    post = db.query(Models.Post, func.count(Models.Like.postId).label("likes")).join(Models.Like,Models.Post.id == Models.Like.postId,isouter=True).group_by(Models.Post.id).filter(Models.Post.ownerId == currUser.id).filter(Models.Post.content.contains(search)).limit(limit).offset(offset).all()

    return post

@router.get("/{id}", response_model=Schemas.PostWithLikes)
def getPost (id : int , db: Session = Depends(get_db), user_id : int = Depends(oauth2.getCurrentUser)):
    post = db.query(Models.Post, func.count(Models.Like.postId).label("likes")).join(Models.Like,Models.Post.id == Models.Like.postId,isouter=True).group_by(Models.Post.id).filter(Models.Post.id == id).first()

    if post == None:    
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id = {id} not found")
    return post
    
@router.delete("/{id}")
def deletePost (id : int , db : Session = Depends(get_db), currUser : int = Depends(oauth2.getCurrentUser)):
    post_query = db.query(Models.Post).filter(Models.Post.id == id)   
    if (post_query.first().ownerId != currUser.id):
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN, detail = "You are not the owner of this post")
    if post_query.first() == None:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail = f"Post with id = {id} not found")
    post_query.delete(synchronize_session = False)
    db.commit()    
    return "deleted successfully"
    
@router.put("/{id}", response_model=Schemas.PostResponse)
def updatePost (id:int, nPost : Schemas.Post, db:Session = Depends(get_db), currUser : int = Depends(oauth2.getCurrentUser) ):
    post_query = db.query(Models.Post).filter(Models.Post.id == id)
    post = post_query.first()
    if (post.ownerId != currUser.id):
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN, detail = "You are not the owner of this post")
    if (post == None):
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id = {id} not found")
    post_query.update(nPost.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
