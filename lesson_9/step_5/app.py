from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def sums(a: int, b: int): # по дефолту ставит строковый тип аргументов
    return a+b