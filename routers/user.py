from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from DataBase import get_db, engine
import Models, Schemas
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix = "/users", tags=["Users"])


@router.get("/", response_model=List[Schemas.UserResponse])
def getUsers (db :Session = Depends(get_db)):
    users = db.query(Models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserResponse)
def addUser ( user : Schemas.UserRequest, db: Session = Depends(get_db)):
    hashedPassword= pwd_context.hash(user.password)
    user.password = hashedPassword
    user1 = Models.User(**user.dict())
    db.add(user1)
    db.commit()
    db.refresh(user1)
    return user1

@router.get("/{id}", response_model=Schemas.UserResponse)
def getUserById (id : int, db: Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.id == id).first()
    if user == None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser (id : int, db : Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.id == id)
    if user.first() == None :
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    user.delete(synchronize_session = False)
    db.commit()
    return "deleted successfully"
    
@router.put("/{id}", response_model = Schemas.UserResponse)
def updateUser (id : int, nUser : Schemas.UserRequest, db: Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.id == id)
    if (user.first()== None):
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id = {id} not found")
    nUser.password= pwd_context.hash(nUser.password)
    user.update(nUser.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user.first())
    return user.first()
    
