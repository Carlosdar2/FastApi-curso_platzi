#python
from typing import Optional
from fastapi.datastructures import Default

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import EmailStr
from enum import  Enum

#FastApi
from fastapi  import Body
from fastapi.param_functions import Form, Query, Path, Header, Cookie
from fastapi import FastAPI
from fastapi import status  
app = FastAPI()



#Models_base
class HairColor(Enum):
    write = 'Write'
    brown = 'Brown'
    black = 'Black'
    blonde = 'Blonde'
    red = 'Red'


class PersonBase(BaseModel):
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
    emal: EmailStr = Field(
        ...,
        
        )
    #personal_blog: HttpUrl = Field(
     #   ...
    #)
    hair_color: Optional[HairColor] = Field(default=None)
    maried: Optional[bool] = Field(default=None)


class FormOut(BaseModel):
    username: str = Field(..., max_length=20, example="Miguel112")

#MODELS
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

class Person(PersonBase): # Person parameters
    password: str = Field(
        ...,
        min_length=8
    )

class Personout(PersonBase):
    pass


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {'Hello':' World '}

#request_response_body
@app.post(
    path='/person/new',
    response_model=Personout,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person


#vadilations +
@app.get(
    path='/person/details/',
    status_code=status.HTTP_202_ACCEPTED
    )
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
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_208_ALREADY_REPORTED
    )
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
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_202_ACCEPTED
    )
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

#Forms
@app.post(
    path='/login',
    response_model= FormOut
)
def login(username: str = Form(...,max_length=20), password: str = Form(..., max_length=7)):
    return FormOut(username=username)


#Cookie and header parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_201_CREATED
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20, 
        min_length=1
    ),
    last_neme: str = Form(
        ...,
        max_length=20,
        min_length=1
         
    ),
    email: EmailStr = Form(...,),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent
