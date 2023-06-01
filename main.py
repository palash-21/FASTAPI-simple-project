from fastapi import FastAPI,Depends,HTTPException,Request,Form
from sqlalchemy.orm import Session
import uvicorn
from fastapi.templating import Jinja2Templates
from database import Base
import crud
from database import Sessionlocal,engine
import schemas 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try :
        yield db
    finally :
        db.close()

@app.get('/',response_class= HTMLResponse)
def base(request:Request):
    return templates.TemplateResponse('base.html',{'request':request})

@app.get("/employees/",response_model=list[schemas.Employee])
def read_employees(request : Request ,skip: int=0,limit: int = 5,db:Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip,limit=limit)
    return templates.TemplateResponse("display_employees.html", {"request" : request ,"employees": employees})

@app.get("/new-employee/", response_class=HTMLResponse)
def new_employee_form(request : Request):
    return templates.TemplateResponse("new_employee.html", {"request" : request})


@app.post('/new-employee/', response_class=HTMLResponse)
def create_employee(request : Request, db:Session= Depends(get_db),  employee_id: int= Form(...) , firstname: str= Form(...) , lastname: str= Form(...) , password: str= Form(...)):
    new_employee = schemas.EmployeeCreate(employee_id=employee_id, firstname=firstname, lastname= lastname, password=password)
    db_employee = crud.get_employee(db, employee_id=new_employee.employee_id)
    if db_employee:
        raise HTTPException(status_code=400, detail = "Employee already registered")
    else :
        crud.create_employee(db=db, employee=new_employee)
    return templates.TemplateResponse("new_employee.html", {"request" : request})

@app.get("/new-task/", response_class=HTMLResponse)
def new_task_form(request : Request):
    return templates.TemplateResponse("new_task.html", {"request" : request})

@app.post('/new-task/', response_class= HTMLResponse)
def create_task_employee(request:Request, db: Session = Depends(get_db), task_id :int = Form(...), description : str = Form(...), owner_id : int = Form(...)):
    new_task = schemas.TaskCreate(task_id = task_id,description=description)
    db_task = crud.get_task(db, task_id=new_task.task_id)
    if db_task:
        raise HTTPException(status_code=400, detail = "Task already created")
    else :
        crud.create_employee_task(db=db, task= new_task , employee_id = owner_id)
    return templates.TemplateResponse('new_task.html', {'request' : request})


@app.get('/tasks/', response_model=list[schemas.Task])
def read_tasks(request: Request,skip:int =0, limit:int =5, db:Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return templates.TemplateResponse("display_tasks.html", {"request" : request ,"tasks": tasks})


# @app.post('/employees/',response_model = schemas.Employee)
# def create_employee(employee:schemas.EmployeeCreate, db:Session= Depends(get_db)):
#     db_employee = crud.get_employee(db,employee_id=employee.employee_id)
#     if db_employee:
#         raise HTTPException(status_code=400, detail = "Employee already registered")
#     return crud.create_employee(db=db, employee=employee)

# @app.get("/employees/",response_model=list[schemas.Employee])
# def read_employees(skip: int=0,limit: int = 5,db:Session = Depends(get_db)):
#     employees = crud.get_employees(db, skip=skip,limit=limit)
#     return employees



# @app.get("/employees/{employee_id}", response_model=schemas.Employee)
# def read_employee(employee_id: int,db:Session = Depends(get_db)):
#     db_employee = crud.get_employee(db=db, employee_id= employee_id )
#     if db_employee is None:
#         raise HTTPException(status_code=404, details = "Employee not found")
#     return db_employee

# @app.post('/employees/{employee_id}/tasks/',response_model = schemas.Task)
# def create_task_for_employee(employee_id : int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
#     db_task = crud.get_task(db,task_id= task.task_id)
#     if db_task:
#         raise HTTPException(status_code=400, detail = "Task already created")
#     return crud.create_employee_task(db=db, task=task, employee_id= employee_id)

# @app.get('/tasks/', response_model=list[schemas.Task])
# def read_tasks(skip:int =0, limit:int =5, db:Session = Depends(get_db)):
#     tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
#     return tasks

if __name__ == "__main__":
    uvicorn.run(app)