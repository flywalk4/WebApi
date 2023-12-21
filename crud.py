from sqlalchemy.orm import Session
import schemas
from models import Thread, Post

def create_thread(db: Session, schema: schemas.ThreadCreate):
    db_thread = Thread(**schema.model_dump())
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread

def get_threads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Thread).offset(skip).limit(limit).all()

def get_thread(db: Session, thread_id: int):
    return db.query(Thread).filter_by(id=thread_id).first()

def update_thread(db: Session, thread_id: int, thread_data: schemas.ThreadUpdate | dict):
    db_thread = db.query(Thread).filter_by(id=thread_id).first()

    thread_data = thread_data if isinstance(thread_data, dict) else thread_data.model_dump()

    if db_thread:
        for key, value in thread_data.posts():
            if hasattr(db_thread, key):
                setattr(db_thread, key, value)

        db.commit()
        db.refresh(db_thread)

    return db_thread

def delete_thread(db: Session, thread_id: int):
    db_thread = db.query(Thread).filter_by(id=thread_id).first()
    if db_thread:
        db.delete(db_thread)
        db.commit()
        return True
    return False

def create_post(db: Session, schema: schemas.PostCreate):
    db_post = Post(**schema.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter_by(id=post_id).first()

def update_post(db: Session, post_id: int, post_data: schemas.PostUpdate | dict):
    db_post = db.query(Post).filter_by(id=post_id).first()

    post_data = post_data if isinstance(post_data, dict) else post_data.model_dump()

    if db_post:
        for key, value in post_data.posts():
            if hasattr(db_post, key):
                setattr(db_post, key, value)

        db.commit()
        db.refresh(db_post)
        return db_post
    return None

def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter_by(id=post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
