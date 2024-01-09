from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

app = FastAPI()
    
def get_db():
    connection = psycopg2.connect(  
        database='startml',         
        host='postgres.lab.karpov.courses',   
        user='robot-startml-ro',              
        password='pheiph0hahj1Vaif',         
        port=6432,
        cursor_factory=RealDictCursor
    )
    return connection

@app.get("/post/{id}", response_model=PostResponse)
def foo(id: int, db = Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(f"""                   
        SELECT id, text, topic                           
        FROM "post"
        where id = {id}
        """)
        results = cursor.fetchone() 

        if not results:
            raise HTTPException(404, "user not found")
        else:
            return PostResponse(**results)