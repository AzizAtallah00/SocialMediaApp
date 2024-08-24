from fastapi import APIRouter, HTTPException, status, Depends
import Schemas, Models, oauth2
from sqlalchemy.orm import Session
from DataBase import get_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router=APIRouter( tags=["Auth"])

@router.post("/login")
def login (nUser:Schemas.UserRequest, db : Session = Depends(get_db) ):
    user = db.query(Models.User).filter(Models.User.email == nUser.email).first()
    if user == None :
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    if pwd_context.verify(nUser.password, user.password) == False:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid password")
    #create token
    return  oauth2.createToken ({'user_id': user.id})

    