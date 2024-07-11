## SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
from database import Base
from sqlalchemy import Column, Integer
from sqlalchemy import String, Boolean

class ToDos(Base):
    
    __tablename__ = "to_do_table"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
