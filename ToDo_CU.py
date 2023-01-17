from _datetime import datetime


class Task:
    def __init__(self, description, status='NEW', start_date=datetime.today(), due_date='NO SET'):
        self.description = description
        self.status = status
        self.start_date = start_date
        self.due_date = due_date

    def __repr__(self):
        return f"{self.description}/{self.status}/{self.start_date}/{self.due_date}"


class TaskStorage:
    def __init__(self, description):
        self.description = description
        self.storage = []

    def add_task(self, task):
        self.storage.append(task)
        print(f'task "{task.description}" added')

    def edit_description(self, task_id, new_description):
        task = self.storage[task_id]
        task.description = new_description

    def set_status(self, task_id, new_status):
        if new_status.upper() not in ['NEW', 'DONE']:
            raise ValueError(f'Wrong status: {new_status}')
        task = self.storage[task_id]
        task.status = new_status.upper()
        print(f'status of "{task.description}" replaced by {new_status.upper()}')

    def show_specific_list(self, specific_status):
        if specific_status.upper() not in ['NEW', 'DONE']:
            raise ValueError(f'Wrong status: {specific_status}')
        for task in self.storage:
            if task.status == specific_status.upper():
                print(f"{specific_status} tasks here: {task.description} - {task.status}")


main_storage = TaskStorage('Main base')

if __name__ == "__main__":

    # main_storage.add_task('lup')
    # main_storage.add_task('pupa')
    # main_storage.add_task('zukko')
    # main_storage.add_task('pipika')
    # main_storage.add_task('hophopa')
    # main_storage.add_task('zhuzhuzhu')

    print(main_storage.storage)  # checking whole the list

    main_storage.set_status(2, 'DONE')        # test editing task status
    main_storage.set_status(4, "DONE")

    print(main_storage.storage)  # checking whole the list whith changes

    main_storage.show_specific_list("done")                # checking how functions work
    # show_archive()
