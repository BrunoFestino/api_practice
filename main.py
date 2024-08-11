from typing import Optional, Union

from fastapi import Body, FastAPI

from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def read_root():

    return {"Hello": "World"}

@app.get("/posts")
def get_post():
    return {"data": "This is your post"}

@app.post("/posts")
def create_posts(post: Post):
    return {"data": f"{post}"}