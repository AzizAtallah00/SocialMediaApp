from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from DataBase import get_db
import Models, oauth2, Schemas


router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/")
def likePost (likedPost : Schemas.likeRequest, currUser : int = Depends(oauth2.getCurrentUser), db : Session = Depends(get_db)):
    post = db.query(Models.Post).filter(Models.Post.id == likedPost.postId).first()
    if post == None :
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id = {likedPost.postId} not found")
    like_query = db.query(Models.Like).filter(Models.Like.userId == currUser.id, Models.Like.postId == likedPost.postId)
    like = like_query.first()
    if (likedPost.dis == False):
        if like != None:
            raise HTTPException (status_code = status.HTTP_409_CONFLICT, detail = "You have already liked this post")
        like = Models.Like(userId = currUser.id, postId = likedPost.postId)
        db.add(like)
        db.commit()
        db.refresh(like)
        return {"message" :  "post successfully liked"}
    else:
        if like == None:
            raise HTTPException (status_code = status.HTTP_400_BAD_REQUEST, detail = "You have not liked this post")
        like_query.delete(synchronize_session = False)
        db.commit()
        return {"message" : "post successfully disliked"}