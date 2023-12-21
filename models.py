from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    posts = relationship('Post', back_populates='thread')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    thread = relationship('Thread', back_populates='posts')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())