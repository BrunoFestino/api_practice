from typing import Optional, Union
from random import randrange
import traceback

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

from App import models
from App.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect("postgresql://postgres:41955162@localhost:5432/fastapi",row_factory=dict_row)
    print("Database connection was succesfull")
except Exception as error:
    print('Error connecting database')
    traceback.print_exc()

my_post = [{
    "title": "title 1",
    "content": "content 1",
    "id": 1
},
{
    "title": "Favorite food",
    "content": "Pizza",
    "id": 2
}]

def find_post(id: int):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id: int):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data": post}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post,db: Session = Depends(get_db)):
    # new_post = conn.execute("INSERT INTO post (title,content,published) VALUES(%s,%s,%s) RETURNING *",(post.title,post.content,post.published)).fetchone()
    # conn.commit()

    

    new_post = models.Post(**post.model_dump())
    print(new_post)

    db.add(new_post)
    
    db.commit()

    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    # post = conn.execute("SELECT * FROM post WHERE id = %s",(str(id),)).fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {} was not found'.format(id))
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):
    # item_deleted = conn.execute("DELETE FROM post WHERE id = %s RETURNING *",(str(id),)).fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {} does not exists'.format(id))
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT,)

@app.put("/posts/{id}")
def update_post(id: int, post: Post,db: Session = Depends(get_db)):
    # updated_record = conn.execute("UPDATE post SET title = %s, content = %s, published = %s where id = %s RETURNING *",(post.title, post.content, post.published, str(id))).fetchone()
    
    post_from_db = db.query(models.Post).filter(models.Post.id == id) 
    if post_from_db.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {} does not exists'.format(id))
    

    post_from_db.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return {'data': post_from_db.first()}
