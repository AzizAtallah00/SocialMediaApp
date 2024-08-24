from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from DataBase import Base
from sqlalchemy.orm import relationship
 
class Post (Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True)
    title = Column (String, nullable=False)
    content = Column (String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text("now()"))
    ownerId = Column (Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User (Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True)
    email = Column (String, nullable=False, unique=True)
    password = Column (String, nullable=False)
    createdAt = Column (TIMESTAMP(timezone=True), nullable=False, server_default = text("now()")) 
    
    
class Like(Base):
    __tablename__ = "likes"
    postId = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
