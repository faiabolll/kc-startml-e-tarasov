from fastapi import FastAPI
from datetime import date, timedelta

app = FastAPI()


@app.get('/')
def sums(a: int, b: int): # по дефолту ставит строковый тип аргументов
    return a+b

@app.get('/sum_date')
def sums(current_date: date, offset: int):
    return current_date + timedelta(days=offset)