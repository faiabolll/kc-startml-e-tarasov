from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(  
    database='startml',         
    host='postgres.lab.karpov.courses',   
    user='robot-startml-ro',              
    password='pheiph0hahj1Vaif',         
    port=6432,
    cursor_factory=RealDictCursor
)
cursor = connection.cursor()  

app = FastAPI()

@app.get("/user/{_id}")
def get_user(_id):
    cursor.execute(f"""                   
    SELECT gender, age, city
    FROM "user"
    where id = {_id}
    """)
    results = cursor.fetchone() 

    # print("213", results)
    if not results:
        raise HTTPException(404, "user not found")
    else:
        return results