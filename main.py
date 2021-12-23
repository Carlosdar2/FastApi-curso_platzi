#python
from typing import Optional
import fastapi
from fastapi.datastructures import Default, UploadFile

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import EmailStr
from enum import  Enum

#FastApi
from fastapi import HTTPException
from fastapi  import Body, UploadFile
from fastapi.param_functions import Form, Query, Path, Header, Cookie, File
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
    username: str = Field(
        ...,
        max_length=20, 
        example="Miguel112")

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
    status_code=status.HTTP_200_OK,
    tags=['Raiz']
    )
def home():
    return {'Hello':' World '}

#request_response_body
@app.post(
    path='/person/new',
    response_model=Personout,
    status_code=status.HTTP_201_CREATED,
    tags= ['Persons'],
    summary='Create Persons in the app'
    )
def create_person(person: Person = Body(...)):
    
    """
        Created Person


        - This path operation creates a person in the app and save the information in the database

        - Parameters:
            Request body parameter:
             - **Person: Person** -> A person model with foirst name, last name , age , hair color and marital status

            - Returns Returns a Person model with foirst name, last name, age, hair color and marital status
    """
    return person


#vadilations +
@app.get(
    path='/person/details/',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Persons']
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
        description=" This is the person age. It's required",
        max_length=33,
        min_length=23,
        
        )
):
    """
        Show Persons


        - This path operation shows a person through the parameters that are indicated

        - Parameters:
            Request body parameter:
             - **Person: Person** -> A person model with foirst name, age 

            - Returns Returns a Person model with foirst name, age
   """
    return {name : age}

#id persons
persons = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#Validations path
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_208_ALREADY_REPORTED,
    tags=['Person_id']
    )
def show_person_id(

    person_id: int = Path(
        ...,
        gt=0, 
        title="Person Id",
        description="This is the person id. It's requiered "
    )
):
    """
        Show Persons for ID


        - This path operation shows a person through the ID from each person

        - Parameters:
            Request body parameter:
             - **Person: Person** -> A person ID

            - Returns Returns a Person model with ID from person
   """
    if person_id not in persons:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This person doesn'texist!"
            )
    return {person_id: 'It exists!'}



#request body
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Person_update']
    )
def updatd_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        descritions ="This is Person ID.",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)

):
    """
        Update Person


        - This path operation updates data of a person who is registered in the database


        - Parameters:
            Request body parameter:
             - **Person: Person** -> To this path operation the parameters person_id, the Person Model and the location are passed


            - Returns: Returns the person with all the updated data that the client has indicated to update
            """

    result = person.dict()
    result.update(location.dict())
    return result

#Forms
@app.post(
    path='/login',
    response_model= FormOut,
    tags=['login']
)
def login(
    username: str = Form(...,max_length=20),
    password: str = Form(..., max_length=7)):
    """
        Update Person


        - This path operation updates data of a person who is registered in the database


        - Parameters:
            Request body parameter:
             - **Person: Person** -> To this path operation the parameters person_id, the Person Model and the location are passed


            - Returns: Returns the person with all the updated data that the client has indicated to update
        """

    return FormOut(username=username)


#Cookie and header parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_201_CREATED,
    tags=['Contact']
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

#files
@app.post(
    path='/post-image',
    tags=['Posts']
)
def post_image(
    image: UploadFile = File(...,)

):

    """
         load Image


        - This path operation load image 


        - Parameters:
            Request body parameter:
             - **Load image** -> content_type and file


            - Returns: Returns the file |that was previously charged
            """

    return {
        'filename': image.filename ,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read())/1024, ndigits=2)
    }