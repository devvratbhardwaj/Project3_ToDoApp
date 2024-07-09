from sqlalchemy import create_engine

## Using SQL Alchemy ORM (which is independent of framework as compared to Django-ORM)
from sqlalchemy.orm import sessionmaker

## 
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args = {'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind = engine)

Base = declarative_base()   ## declarative_base returns a class
                            ## so Base is a class
