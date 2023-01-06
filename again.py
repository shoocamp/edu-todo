class Task:
    def __init__(self, description, status='new'):
        self.description = description
        self.status = status

    def __repr__(self):
            return f"{self.description} - {self.status}"


class Base:
    def __init__(self, description):
        self.description = description
        self.storage = []


main_base = Base('Main base')


def add_task(descriprion):
    task = Task(descriprion)
    main_base.storage.append(task)
    print(f'task "{descriprion}" added')


def set_status_done(task_id):
    task = main_base.storage[task_id]
    task.status = 'done'
    print(f'status of "{task.description}" replaced DONE')


def show_new():
    for t in main_base.storage:
        if t.status == "done":
            continue
        else:
            print(f"{t.description} - {t.status}")


def show_archive():
    for t in main_base.storage:
        if t.status == "new":
            continue
        else:
            print(f"{t.description} - {t.status}")


add_task('lup')
add_task('pupa')
add_task('zukko')
add_task('pipika')
add_task('hophopa')
add_task('zhuzhuzhu')

print(main_base.storage)  # checking whole the list

set_status_done(2)        # test editing task status
set_status_done(4)

print(main_base.storage)  # checking whole the list whith changes

show_new()                # checking how functions work
show_archive()