from todo_cu import Task, TaskStorage
from ui import CLIHandler
import pytest
from datetime import datetime as dt


def test_task_creation():
    dscr = 'somewords'
    task = Task(dscr)
    assert task.description == dscr
    assert task.due_date is None
    assert task.status == 'NEW'


def test_task_creation_empty():
    dscr = ''
    with pytest.raises(ValueError):
        task = Task(dscr)


def test_update_dscr():
    task = Task('first dscr')
    new_dscr = "test dscr"
    task.update_description(new_dscr)
    assert task.description == new_dscr


def test_update_dscr_empty():
    task = Task('first dscr')
    new_dscr = ""
    try:
        task.update_description(new_dscr)
    except ValueError:
        pass
    else:
        raise RuntimeError("")


def test_update_status():
    task = Task('any dscr')
    assert task.status == "NEW"
    new_status = "done"
    task.update_status(new_status)
    assert task.status == new_status.upper()


def test_update_status_no_valid():
    task = Task('any dscr')
    assert task.status == "NEW"
    new_status = "OLD"
    try:
        task.update_status(new_status)
    except ValueError:
        pass


def test_update_due_date():
    task = Task('any dscr')
    due_date = dt.strptime("27 February, 2023", "%d %B, %Y")
    task.update_due_date(due_date)
    assert task.due_date == due_date


def test_update_due_date_error():
    task = Task('any dscr')
    due_date = "27 February 2023"   #  not dt.strptime("", "%d %B %Y")
    with pytest.raises(ValueError):
        task.update_due_date(due_date)


"""Tests for TaskStorage Class"""


def test_storage_creation():
    test_dscr = "test storage"
    test_storage = TaskStorage(test_dscr)
    assert test_storage.description == test_dscr


def test_add_task():
    task = Task('any dscr')
    storage = TaskStorage('any dscr')
    storage.add_task(task)
    assert storage.storage[0] == task


def test_get_task_by_id():
    storage = TaskStorage('any dscr')
    storage.storage = [1,2,3,4]
    task_id = 2
    assert storage.get_task_by_id(task_id-1) == task_id


def test_get_task_by_id_error():
    storage = TaskStorage('any dscr')
    storage.storage = [1, 2, 3, 4, 5, 6, 7]
    task_id = 8
    with pytest.raises(ValueError):
        storage.get_task_by_id(task_id - 1)

storage = TaskStorage('any dscr')   # надо было так сделать в начале тестов класса ТаскСтораж. Передалать?
t1 = Task('any dscr1')
t2 = Task('any dscr2')
t3 = Task('any dscr3')
storage.storage.append(t1)
storage.storage.append(t2)
storage.storage.append(t3)

def test_edit_description():
    new_dscr = "new dscr"
    task_id = 1
    storage.edit_description(task_id, new_dscr)
    assert t2.description == new_dscr


def test_edit_status():
    new_status = "done"
    task_id = 1
    storage.set_task_status(task_id, new_status)
    assert t2.status == new_status.upper()


def test_filter_tasks_by_status():
    test_status = "DONE"
    t2.status = test_status
    test_storage = []
    test_storage.append(t2)
    assert storage.filter_tasks_by_status(test_status) == test_storage


def test_get_size():
    assert storage.get_size() == 3


def test_is_emty():
    assert storage.is_list_empty() == False


"""Tests for ui.py"""
# раздел в разработке :)