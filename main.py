#python

from typing import Optional
#pydantic

from fastapi  import Body
from fastapi.param_functions import Query, Path
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
    name: Optional[str] = Query(
    None, 
    min_length=1,
    max_length=10,
    title='Person name', 
    description=" This is the person name, It's  between 1 and 50 characters"

    ),
    age: str = Query(
        ..., 
        title="Person Age",
        description=" This is the person age. It's required"
        )
):
    return {name : age}

#Validations path
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0, 
        title="Person Id",
        description="This is the person id. It's requiered"

        )
):
    return {person_id: 'It exists!'}
