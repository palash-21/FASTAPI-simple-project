from pydantic import BaseModel
#from dataclasses import dataclass
#from fastapi import Form

class TaskBase(BaseModel):
    description  : str

class TaskCreate(TaskBase):
    task_id : int

class Task(TaskBase):
    task_id : int
    owner_id : int
    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    firstname : str
    lastname : str


class EmployeeCreate(EmployeeBase):
    employee_id : int
    password : str

# @dataclass
# class EmployeeCreate(BaseModel):
#     employee_id : int = Form(...)
#     firstname : str = Form(...)
#     lastname : str = Form(...)
#     password : str = Form(...)


class Employee(EmployeeBase):
    employee_id : int 
    tasks : list[Task] = []

    class Config:
        orm_mode = True




     