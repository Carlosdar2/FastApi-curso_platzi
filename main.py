#python

from typing import Optional
#pydantic

from fastapi  import Body
from fastapi.param_functions import Query, Path
from pydantic import BaseModel
from enum import  Enum
from pydantic import Field
 #FastApi
from fastapi import FastAPI
from pydantic.networks import EmailStr, HttpUrl
from pydantic.types import PaymentCardBrand


app = FastAPI()

#models
class HairColor(Enum):
    write = 'Write'
    brown = 'Brown'
    black = 'Black'
    blonde = 'Blonde'
    red = 'Red'


class  Location(BaseModel):
    city: str = Field(
        ...,
    )
    state : str = Field(
        ...,
    )
    country: str = Field(
        ...,
    )

class Person(BaseModel): # Person parameters
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    age_person: int = Field(
        gt=0,
        le=100
    )
    emal: EmailStr
    personal_blog = HttpUrl
    hair_color: Optional[HairColor] = Field(default=None)
    maried: Optional[bool] = Field(default=None)
    
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
        description="This is the person id. It's requiered "
    )
):
    return {person_id: 'It exists!'}



#request body
@app.put('/person/{person_id}')
def udatd_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        descritions ="This is Person ID.",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)

):
    result = person.dict()
    result.update(location.dict())
    return result