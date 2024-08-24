from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
import jwt, Schemas
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def createToken (data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm =ALGORITHM)
    return {"token" : encoded_jwt, "type" : "bearer"}

def verifyToken (token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id == None:
            raise credentials_exception
        token_data = Schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
def getCurrentUser (token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return verifyToken(token, credentials_exception)
