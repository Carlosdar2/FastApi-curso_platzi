#python

from typing import Optional
#pydantic

from fastapi  import Body
from fastapi.param_functions import Query
from pydantic import BaseModel


 #FastApi
from fastapi import FastAPI

app = FastAPI()


class Person(BaseModel): # Person parameters
    first_name: str
    last_name: str
    age_person: int
    color: Optional[str] = None
    maried: Optional[bool] = None
    
@app.get("/")
def home():
    return {'Hello':' World '}

#request_response_bodye

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person
#vadilations +
@app.get('/person/details/')
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=10),
    age: str = Query(...)
):
    return {name : age}
