from typing import Annotated
from fastapi import Depends, FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Boolean
from starlette import status
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import ToDos

app = FastAPI()

models.Base.metadata.create_all(bind = engine)
## Will not run automatically if the database already exists

def get_db():
    db = SessionLocal() ## Contact the database
    try:
        yield db        ## Open database only while using
    finally:
        db.close()      ## and close it afterwards

## Depends -> Dependency injection: read_all method relies on the get_db method
db_dependency = Annotated[Session, Depends(get_db)]

class ToDoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=101)
    priority : int = Field(gt=-1, lt=11)
    complete: bool = Field(default=False)

@app.get("/", status_code=status.HTTP_200_OK)           
async def read_all(db: db_dependency): ## from typing import Annotated
    return db.query(ToDos).all()        ## from sqlalchemy.orm import session
                                  ## from fastapi import Depend
                                
@app.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, id:int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == id).first() ## return as soon as there is a match
    if todo_model != None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/addtolist", status_code= status.HTTP_201_CREATED)
async def add_item(db: db_dependency, item:ToDoRequest):
    todo_model = ToDos(**item.model_dump())
    db.add(todo_model)
    db.commit()

@app.put("/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item(db:db_dependency, item:ToDoRequest, id:int = Path(gt=0)):
    
    todo_model = db.query(ToDos).filter(ToDos.id == id).first()

    if todo_model == None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    todo_model.title = item.title
    todo_model.description = item.description
    todo_model.priority = item.priority
    todo_model.complete = item.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_db(db:db_dependency, id:int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Not Found")
    db.query(ToDos).filter(ToDos.id==id).delete()
    db.commit()
    
