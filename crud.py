from sqlalchemy.orm import Session

from schemas import EmployeeCreate,TaskCreate
from models import Tasks,Employee

def get_employee(db: Session, employee_id :int):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()


# def get_employee_by_firstname(db :Session, firstname:str):
#     return db.query(Employee).filter(Employee.firstname == firstname).first()

def get_employees(db: Session, skip: int = 0, limit: int =5):
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db:Session, employee: EmployeeCreate ):
    fake_hashed_password = employee.password + "not_really_hashed"
    db_employee = Employee(employee_id = employee.employee_id,firstname = employee.firstname, lastname = employee.lastname, hashed_password = fake_hashed_password)
    db.add(db_employee)
    db.commit()
    return db_employee

def get_tasks(db:Session, skip: int=0, limit: int = 5):
    return db.query(Tasks).offset(skip).limit(limit).all()

def get_task(db:Session, task_id : int):
    return db.query(Tasks).filter(Tasks.task_id == task_id).first()

def create_employee_task(db:Session, task : TaskCreate,employee_id :int):
    db_task = Tasks(**task.dict(), owner_id = employee_id)
    db.add(db_task)
    db.commit()
    return db_task

    