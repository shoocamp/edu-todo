from todo_cu import Task
from ui import CLIHandler


def test_task_creation():
    dscr = 'somewords'
    task = Task(dscr)
    assert task.description == dscr, 'yra!!!'  # it doesn`t appear in tracebook!!!
    assert task.due_date is None
    assert task.status == 'NEW'


def test_task_creation_empty():
    dscr = ''
    try:
        task = Task(dscr)  # may I leave it like it is?
    except ValueError:
        pass


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
        raise RuntimeError("")  # what`s this?


def test_update_status():
    task = Task('any dscr')
    assert task.status == "NEW"
    new_status = "done"
    task.update_status(new_status)
    assert task.status.lower() == new_status  # tricky or bullshit?


def test_update_status_no_valid():
    task = Task('any dscr')
    assert task.status == "NEW"
    new_status = "OLD"
    try:
        task.update_status(new_status)
    except ValueError:
        pass
