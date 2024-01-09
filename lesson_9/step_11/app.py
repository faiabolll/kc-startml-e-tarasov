from fastapi import FastAPI, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor

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

@app.get("/user/{_id}")
def foo(_id: int, db = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(f"""                   
        SELECT gender, age, city
        FROM "user"
        where id = {_id}
        """)
        results = cursor.fetchone() 

        if not results:
            raise HTTPException(404, "user not found")
        else:
            return results