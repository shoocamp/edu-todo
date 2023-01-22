from datetime import datetime


class Task:
    def __init__(self, description, status='NEW', start_date=datetime.today(), due_date='NO SET'):
        self.description = description
        self.status = status
        self.start_date = start_date
        self.due_date = due_date

    def __repr__(self):
        return f'{self.description}/{self.status}/{self.start_date.strftime("%d.%m.%y - %H.%M")}/{self.due_date}'


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

    def set_task_status(self, task_id, new_status):
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

    def tasks_with_idexes(self):
        result = []  # нормально если этим методом сделают новый список?
        for (i, item) in enumerate(self.storage, start=1):
            result.append(f'{str(i)}: {item}')
        return result

    def is_list_empty(self):
        if len(self.storage) == 0:
            return True
        else:
            return False


main_storage = TaskStorage('Main base')

if __name__ == "__main__":
    print(main_storage.storage)

    task_1 = Task("popa")
    task_2 = Task("kloklo")
    main_storage.add_task(task_1)
    main_storage.add_task(task_2)
    main_storage.set_task_status(1, 'done')

    print(main_storage.tasks_with_idexes())
    print(main_storage.show_specific_list('done'))