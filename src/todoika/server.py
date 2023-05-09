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
    user_name = credentials.username
    user_id = storage.get_user_by_name(user_name)[0]
    return user_id


@app.post("/list_id/{list_id}/add_task")
def add_task(user_id: Annotated[str, Depends(get_current_username)],
             list_id: int, data: dict[str, str]):
    task_description = data.get('task_description')
    if data.get('due_date'):
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d, %H:%M')
        task_db_id = storage.add_task(user_id, list_id, description=task_description, status="NEW", due_date=due_date)
    else:
        task_db_id = storage.add_task(user_id, list_id, description=task_description, status="NEW", due_date=None)
    task = storage.get_task_by_id(task_db_id)
    task_list.tasks.append(task)
    return task


@app.put("/task/{task_id}/")
def edit_task(user_id: Annotated[str, Depends(get_current_username)],
              task_id: int, data: dict[str, str]):
    if data.get('new_description'):
        new_description = data.get('new_description')
        storage.update_task(task_id=task_id, description=new_description)
        task = storage.get_task_by_id(task_id)
    if data.get('new_status'):
        new_status = data.get('new_status')
        storage.update_task(task_id=task_id, status=new_status)
        task = storage.get_task_by_id(task_id)
    if data.get('new_due_date'):
        new_date: datetime = datetime.strptime(data.get('new_due_date'), '%Y-%m-%d, %H:%M')
        storage.update_task(task_id=task_id, due_date=new_date)
        task = storage.get_task_by_id(task_id)
    return task


@app.get("/list/{list_id}")
def get_tasks(user_id: Annotated[str, Depends(get_current_username)],
              list_id: int, status: Optional[str] = None):
    result = storage.get_tasks_by_status(list_id, status)
    return result
