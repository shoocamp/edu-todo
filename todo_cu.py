from datetime import datetime


class Task:
    VALID_STATUSES = ["NEW", "DONE"]

    def __init__(self, description, due_date=None):
        self.status = "NEW"

        if description == "":
            raise ValueError("Description shouldn't be empty")

        self.description = description
        self.created = datetime.now()
        self.due_date = due_date

    def update_description(self, description):
        if description == "":
            raise ValueError("Description shouldn't be empty")
        self.description = description

    def update_status(self, status):
        status = status.upper()
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}', valid options: {self.VALID_STATUSES}")
        self.status = status

    def update_due_date(self, due_date):
        if not isinstance(due_date, datetime):
            raise ValueError(f"due_date should be a datetime object, got: {due_date} ({type(due_date)})")
        self.due_date = due_date

    def __repr__(self):
        return (f"{self.description}/{self.status}/"
                f"{self.created.strftime('%d.%m.%y - %H.%M')}/"
                f"{self.due_date.strftime('%d.%m.%y - %H.%M') if self.due_date else ''}")


class TaskStorage:
    def __init__(self, description):
        self.description = description
        self.storage = []

    def add_task(self, task):
        self.storage.append(task)

    def get_task_by_id(self, task_id):
        if (len(self.storage) - 1) < task_id < 0:
            raise ValueError(f"Invalid task id: {task_id}")
        return self.storage[task_id]

    def edit_description(self, task_id, new_description):
        task = self.get_task_by_id(task_id)
        task.update_description(new_description)

    def set_task_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        task.update_status(new_status)

    def filter_tasks_by_status(self, status):
        if status is None:
            return self.storage
        status = status.upper()
        tasks = []
        for task in self.storage:
            if task.status == status:
                tasks.append(task)
        return tasks

    def get_size(self):
        return len(self.storage)

    def __repr__(self):
        return "\n".join(map(str, self.storage))

    def is_list_empty(self):
        return len(self.storage) == 0

def get_default_storage():
    return TaskStorage('Default')


if __name__ == "__main__":
    main_storage = get_default_storage()

    print(main_storage.storage)

    task_1 = Task("popa")
    task_2 = Task("kloklo")
    main_storage.add_task(task_1)
    main_storage.add_task(task_2)
    main_storage.set_task_status(1, 'done')

    print(main_storage.filter_tasks_by_status('done'))
