from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key =True, index=True)
    firstname = Column(String,index=True)
    lastname = Column(String,index=True)
    hashed_password = Column(String)
    tasks = relationship('Tasks',back_populates = 'owner')

class Tasks(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key = True,index=True)
    description = Column(String,index=True)
    owner_id = Column(Integer, ForeignKey("employees.employee_id"))

    owner = relationship('Employee', back_populates = 'tasks')

