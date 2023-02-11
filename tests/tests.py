from todo_cu import Task, TaskStorage

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
    with pytest.raises(ValueError):
        task.update_description(new_dscr)


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
    with pytest.raises(ValueError):
        task.update_status(new_status)


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


@pytest.fixture()
def list_for_tests():
    storage = TaskStorage('any dscr')   # Похоже?))
    t1 = Task('any dscr1')
    t2 = Task('any dscr2')
    t3 = Task('any dscr3')
    storage.storage.append(t1)
    storage.storage.append(t2)
    storage.storage.append(t3)
    print(storage.storage)
    return storage


def test_edit_description(list_for_tests):
    new_dscr = "new dscr"
    task_id = 1
    storage = list_for_tests
    storage.edit_description(task_id, new_dscr)
    t2 = storage.storage[task_id]
    assert t2.description == new_dscr


def test_edit_status(list_for_tests):
    new_status = "done"
    task_id = 1
    list_for_tests.set_task_status(task_id, new_status)
    assert list_for_tests.storage[task_id].status == new_status.upper()


def test_filter_tasks_by_status(list_for_tests):
    test_status = "DONE"
    t2 = list_for_tests.storage[1]
    t2.status = test_status
    test_storage = []
    test_storage.append(t2)
    assert list_for_tests.filter_tasks_by_status(test_status) == test_storage


def test_get_size(list_for_tests):
    assert list_for_tests.get_size() == 3


def test_is_emty(list_for_tests):
    assert list_for_tests.is_list_empty() == False


"""Tests for ui.py"""
# раздел в разработке :)