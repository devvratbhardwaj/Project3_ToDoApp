from typing import Annotated
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)
## Will not run automatically if the database already exists

def get_db():
    db = SessionLocal()
    try:
        yield db        ## Open database only while using
    finally:
        db.close()      ## and close it afterwards

## PICK UP RIGHT HERE

@app.get("/")
async def read_all(db:Annotated[Session, ]): ## from typing import Annotated
                                  ## from sqlalchemy.orm import session
                                  ## from fastapi import Depends

