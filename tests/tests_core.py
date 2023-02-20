from datetime import datetime as dt, timedelta

import pytest

from todoika.core import Task, TasksList
from todoika.storage import SQLiteStorage, UserBuilder


@pytest.fixture()
def in_memory_storage():
    storage = SQLiteStorage(":memory:")
    storage.con.executescript(open("../scripts/init_db.sql").read())
    storage.con.commit()
    return storage


@pytest.fixture()
def user(in_memory_storage):
    user_builder = UserBuilder(in_memory_storage)
    return user_builder.build_new('test_user', 'test_password')


@pytest.fixture()
def default_todo_list(in_memory_storage, user):
    default_list = TasksList('Test Default', db_id=user.default_list_id, storage=in_memory_storage, user_id=user.db_id)
    default_list.add_task('Test task 1')
    default_list.add_task('Test task 2')
    default_list.add_task('Test task 3')
    return default_list


def test_task_creation():
    dscr = 'some words'
    task = Task(dscr)
    assert task.description == dscr
    assert task.due_date is None
    assert task.status == 'NEW'


def test_task_creation_empty():
    dscr = ''
    with pytest.raises(ValueError):
        Task(dscr)


def test_update_dscr(default_todo_list, in_memory_storage):
    task = default_todo_list.get_task_by_id(0)
    new_dscr = "test dscr"
    task.description = new_dscr
    assert task.description == new_dscr
    _, actual_description, *_ = in_memory_storage.get_task_by_id(task._db_id)
    assert new_dscr == actual_description


def test_update_dscr_empty(default_todo_list):
    task = default_todo_list.get_task_by_id(0)
    new_dscr = ""
    with pytest.raises(ValueError):
        task.description = new_dscr


def test_update_status(default_todo_list, in_memory_storage):
    task = default_todo_list.get_task_by_id(0)
    assert task._status == "NEW"
    new_status = "DONE"
    task.status = new_status
    assert task._status == new_status
    _, _, actual_status, *_ = in_memory_storage.get_task_by_id(task._db_id)
    assert new_status == actual_status


def test_update_status_no_valid():
    task = Task('any dscr')
    assert task.status == "NEW"
    new_status = "OLD"
    with pytest.raises(ValueError):
        task.status = new_status


def test_update_due_date(default_todo_list, in_memory_storage):
    task = default_todo_list.get_task_by_id(0)
    new_due_date = dt.strptime("27 February, 2023", "%d %B, %Y")
    task.due_date = new_due_date
    assert task.due_date == new_due_date
    _, _, _, _, due_date_ts, *_ = in_memory_storage.get_task_by_id(task._db_id)
    assert new_due_date == dt.fromtimestamp(due_date_ts)


def test_update_due_date_error():
    task = Task('any dscr')
    due_date = "27 February 2023"  # not `datetime`
    with pytest.raises(ValueError):
        task.due_date = due_date


def test_add_task(default_todo_list, in_memory_storage):
    expected_task = default_todo_list.add_task("Test Task", due_date=dt.now())
    assert default_todo_list.get_task_by_id(len(default_todo_list) - 1) == expected_task
    _, description, status, created_ts, due_date_ts, _, _, _ = in_memory_storage.get_task_by_id(expected_task._db_id)

    assert expected_task.description == description
    assert expected_task.status == status
    assert int(expected_task._created.timestamp()) == created_ts
    assert int(expected_task.due_date.timestamp()) == due_date_ts

    new_due_date = dt.now() + timedelta(days=1)
    new_description = "new description"
    new_status = "DONE"

    expected_task.description = new_description
    expected_task.status = new_status
    expected_task.due_date = new_due_date

    _, description, status, _, due_date_ts, _, _, _ = in_memory_storage.get_task_by_id(expected_task._db_id)
    assert description == new_description
    assert status == new_status
    assert int(due_date_ts) == int(new_due_date.timestamp())


def test_get_task_by_id_1(default_todo_list):
    task = default_todo_list[0]
    assert default_todo_list.get_task_by_id(1, start=1) == task


def test_get_task_by_id_2(default_todo_list):
    task = default_todo_list[2]
    assert default_todo_list.get_task_by_id(3, start=1) == task


def test_get_task_by_id_3(default_todo_list):
    task = default_todo_list[2]
    assert default_todo_list.get_task_by_id(2, start=0) == task


def test_get_task_by_id_error_1(default_todo_list):
    with pytest.raises(ValueError):
        default_todo_list.get_task_by_id(0, start=1)


def test_get_task_by_id_error_2(default_todo_list):
    with pytest.raises(ValueError):
        default_todo_list.get_task_by_id(4, start=1)


def test_get_task_by_id_error_3(default_todo_list):
    with pytest.raises(ValueError):
        default_todo_list.get_task_by_id(3, start=0)


def test_edit_description(default_todo_list):
    new_dscr = "new dscr"
    task_id = 1
    storage = default_todo_list
    storage.edit_task_description(task_id, new_dscr)
    t2 = storage.get_task_by_id(task_id)
    assert t2.description == new_dscr


def test_edit_status(default_todo_list):
    new_status = "done"
    task_id = 1
    default_todo_list.set_task_status(task_id, new_status)
    assert default_todo_list.get_task_by_id(task_id).status == new_status.upper()


def test_filter_tasks_by_status(default_todo_list):
    test_status = "DONE"
    t2 = default_todo_list.get_task_by_id(1)
    t2.status = test_status
    test_storage = [t2]
    assert default_todo_list.filter_tasks_by_status(test_status) == test_storage


def test_filter_tasks_by_status_all(default_todo_list):
    assert default_todo_list.filter_tasks_by_status(None) == default_todo_list._tasks


def test_get_size(default_todo_list):
    assert len(default_todo_list) == 3


def test_is_empty(default_todo_list):
    assert not default_todo_list.is_empty()


def test_build_list_from_db(in_memory_storage, user, default_todo_list):
    list_db_id, description, _ = in_memory_storage.get_list(user.default_list_id)
    related_tasks = in_memory_storage.get_tasks_for_list_id(list_db_id)
    actual = TasksList.from_db(description, in_memory_storage, list_db_id, user.db_id, related_tasks)
    assert actual._tasks == default_todo_list._tasks
