from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_thread, get_threads, get_thread, update_thread, delete_thread,
    create_post, get_posts, get_post, update_post, delete_post
)

router_websocket = APIRouter()
router_threads = APIRouter(prefix='/threads', tags=['thread'])
router_posts = APIRouter(prefix='/posts', tags=['post'])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)

@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"#{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"#{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f" #{client_id} left the chat")

@router_threads.post("/", response_model=schemas.Thread)
async def create_thread_route(thread_data: schemas.ThreadCreate, db: Session = Depends(get_db)):
    thread = create_thread(db, thread_data)
    await notify_clients(f"Thread added: {thread.name}")
    return thread

@router_threads.get("/", response_model=List[schemas.Thread])
async def read_threads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    threads = get_threads(db, skip=skip, limit=limit)
    return threads

@router_threads.get("/{thread_id}", response_model=schemas.Thread)
async def read_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = get_thread(db, thread_id)
    return thread

@router_threads.patch("/{thread_id}", response_model=schemas.Thread)
async def update_thread_route(thread_id: int, thread_data: schemas.ThreadUpdate, db: Session = Depends(get_db)):
    updated_thread = update_thread(db, thread_id, thread_data)
    if updated_thread:
        await notify_clients(f"Thread updated: {updated_thread.name}")
        return updated_thread
    return {"message": "Thread not found"}

@router_threads.delete("/{thread_id}")
async def delete_thread_route(thread_id: int, db: Session = Depends(get_db)):
    deleted = delete_thread(db, thread_id)
    if deleted:
        await notify_clients(f"Thread deleted: ID {thread_id}")
        return {"message": "Thread deleted"}
    return {"message": "Thread not found"}

@router_posts.post("/", response_model=schemas.Post)
async def create_post_route(schema: schemas.PostCreate, db: Session = Depends(get_db)):
    post = create_post(db, schema)
    await notify_clients(f"Post added: {post.name}")
    return post

@router_posts.get("/", response_model=List[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts

@router_posts.get("/{post_id}", response_model=schemas.Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    return post

@router_posts.patch("/{post_id}")
async def update_post_route(post_id: int, schema: schemas.PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post(db, post_id, schema)
    if updated_post:
        await notify_clients(f"Post updated: {updated_post.name}")
        return updated_post
    return {"message": "Post not found"}

@router_posts.delete("/{post_id}")
async def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    deleted = delete_post(db, post_id)
    if deleted:
        await notify_clients(f"Post deleted: ID {post_id}")
        return {"message": "Post deleted"}
    return {"message": "Post not found"}