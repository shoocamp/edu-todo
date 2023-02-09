from datetime import datetime


class Task:
    VALID_STATUSES = ["NEW", "DONE"]

    def __init__(self, description, due_date=None, db_id=None, storage=None):
        self.status = "NEW"

        if description == "":
            raise ValueError("Description shouldn't be empty")

        self.description = description
        self.created = datetime.now()
        self.due_date = due_date
        self.storage = storage
        self.db_id = db_id

    def update_description(self, description):
        if description == "":
            raise ValueError("Description shouldn't be empty")
        self.description = description
        if self.storage is not None and self.db_id is not None:
            self.storage.update_task(self.db_id, description=description)

    def update_status(self, status):
        status = status.upper()
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}', valid options: {self.VALID_STATUSES}")
        self.status = status
        if self.storage is not None and self.db_id is not None:
            self.storage.update_task(self.db_id, status=status)

    def update_due_date(self, due_date):
        if not isinstance(due_date, datetime):
            raise ValueError(f"due_date should be a datetime object, got: {due_date} ({type(due_date)})")
        self.due_date = due_date
        if self.storage is not None and self.db_id is not None:
            self.storage.update_task(self.db_id, due_date=due_date)

    def __repr__(self):
        return (f"{self.description}/{self.status}/"
                f"{self.created.strftime('%d.%m.%y - %H.%M')}/"
                f"{self.due_date.strftime('%d.%m.%y - %H.%M') if self.due_date else ''}")


class TasksList:
    def __init__(self, description, db_id=None, storage=None, user_id=None):
        self.description = description
        self.tasks = []
        if storage and not (db_id and user_id):
            raise RuntimeError("`db_id` and `user_id` must be set if `storage` is not `None`")
        self.storage = storage
        self.db_id = db_id
        self.user_id = user_id

    def add_task(self, task, save=True):
        self.tasks.append(task)
        if self.storage is not None and save:
            self.storage.add_task(self.user_id, self.db_id, task.description, task.status, task.due_date)

    def get_task_by_id(self, task_id):
        if 0 <= task_id <= len(self.tasks) - 1:
            return self.tasks[task_id]

        raise ValueError(f"Invalid task id: {task_id}")

    def edit_description(self, task_id, new_description):
        task = self.get_task_by_id(task_id)
        task.update_description(new_description)

    def set_task_status(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        task.update_status(new_status)

    def filter_tasks_by_status(self, status):
        if status is None:
            return self.tasks
        status = status.upper()
        tasks = []
        for task in self.tasks:
            if task.status == status:
                tasks.append(task)
        return tasks

    def get_size(self):
        return len(self.tasks)

    def __repr__(self):
        return "\n".join(map(str, self.tasks))

    def is_empty(self):
        return len(self.tasks) == 0
