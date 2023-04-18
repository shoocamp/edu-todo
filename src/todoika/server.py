from datetime import datetime
import hashlib
from typing import Optional

import toml
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

from todoika.core import TasksList
from todoika.storage import UserBuilder, TasksListBuilder, PSQLStorage


conf = toml.load("./src/todoika/psql_config.toml")
storage = PSQLStorage(host=conf['database']['host'],
                      user=conf['database']['user'],
                      password=conf['database']['password'],
                      db_name=conf['database']['db_name'],
                      port=conf['database']['port'])

user_build = UserBuilder(storage)
task_l_builder = TasksListBuilder(storage)
task_list = TasksList('default')

app = FastAPI()
security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username = credentials.username
    current_password = credentials.password
    password_hash = hashlib.md5(current_password.encode()).hexdigest()
    password_hash_from_db = storage.get_md5hash_by_name(current_username)
    is_correct_password = secrets.compare_digest(
        password_hash, password_hash_from_db
        )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/userid/{user_id}/listid/{list_id}/description/{task_description}")
def add_task(user_id: int, list_id: int, task_description, due_date: Optional[datetime] = None):
    task_db_id = storage.add_task(user_id, list_id, description=task_description, status="NEW", due_date=due_date)
    task = storage.get_task_by_id(task_db_id)
    task_list.tasks.append(task)
    return task


@app.post("/descr")
def edit_description(username: Annotated[str, Depends(get_current_username)],
                     task_id: int, new_description):
    storage.update_task(task_id=task_id, description=new_description)
    task = storage.get_task_by_id(task_id)
    return username, task


@app.post("/taskid/{task_id}/status/{new_status}")
def set_task_status(task_id: int, new_status):
    storage.update_task(task_id=task_id, status=new_status)
    task = storage.get_task_by_id(task_id)
    return task


@app.post("/taskid/{task_id}/due_date/{date}")
def edit_due_date(task_id: int, date):
    new_date: datetime = datetime.strptime(date, '%Y-%m-%d, %H:%M')
    storage.update_task(task_id=task_id, due_date=new_date)
    task = storage.get_task_by_id(task_id)
    return task


@app.get("/tasks/{list_id}/status/{status}")
def show_tasks_by_status(list_id: int, status: str):
    result = storage.get_tasks_by_status(list_id, status)
    return result


@app.get("/tasks/{list_id}")
def show_all_tasks(list_id: int):
    result = storage.get_tasks_by_status(list_id)
    return result
