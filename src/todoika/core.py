from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from todoika.storage import Storage


class Task:
    VALID_STATUSES = ["NEW", "DONE"]

    def __init__(self,
                 description: str,
                 due_date: Optional[datetime] = None,
                 db_id: Optional[int] = None,
                 storage: Optional['Storage'] = None,
                 status="NEW"):
        self._status = status
        self._created = datetime.now()
        self._due_date = due_date
        self.__storage = storage
        self._db_id = db_id
        self.description = description

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: str):
        status = status.upper()
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}', valid options: {self.VALID_STATUSES}")
        self._status = status
        if self.__storage is not None and self._db_id is not None:
            self.__storage.update_task(self._db_id, status=status)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        if new_description == "":
            raise ValueError("Description shouldn't be empty")
        self._description = new_description
        if self.__storage is not None and self._db_id is not None:
            self.__storage.update_task(self._db_id, description=new_description)

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, new_date: datetime):
        if not isinstance(new_date, datetime):
            raise ValueError(f"due_date should be a datetime object, got: {new_date} ({type(new_date)})")
        self._due_date = new_date
        if self.__storage is not None and self._db_id is not None:
            self.__storage.update_task(self._db_id, due_date=new_date)

    def __repr__(self):
        return (f"{self.__class__.__name__}(description={self._description}, "
                f"due_date={self._due_date}, db_id={self._db_id}, "
                f"storage={self.__storage}, status={self._status}), created={self._created}")

    def __str__(self):
        return f"{self._status:5}{self._description}\t{self.due_date if self.due_date else ''}"

    def __eq__(self, other):
        return (self.description == other.description and
                self.status == other.status and
                self.due_date == other.due_date)


class TasksList:
    def __init__(self,
                 description: str, db_id: Optional[int] = None,
                 storage: Optional['Storage'] = None,
                 user_id: Optional[int] = None):
        self._description = description
        self._tasks: list[Task] = []

        if any((storage, db_id)) and not all((storage, db_id, user_id)):
            raise RuntimeError("`db_id`, `storage` and `user_id` must be set if `storage` or `db_id` is not `None`")

        self.__storage = storage
        self.__db_id = db_id
        self.__user_id = user_id

    @classmethod
    def from_db(cls, description: str, storage: 'Storage', db_id: int, user_id: int, tasks: list[tuple]):
        lst = cls(description, db_id, storage, user_id)
        for task_db_id, description, status, created_ts, due_date_ts, _, _, _ in tasks:
            task = Task(description, storage=storage, db_id=task_db_id, status=status)
            lst._tasks.append(task)

        return lst

    def add_task(self, task_description: str, due_date: Optional[datetime] = None) -> Task:
        if self.__storage:
            task_id = self.__storage.add_task(self.__user_id, self.__db_id, task_description, "NEW", due_date)
            task = Task(task_description, due_date, storage=self.__storage, db_id=task_id)
        else:
            task = Task(task_description, due_date)

        self._tasks.append(task)
        return task

    def get_task_by_id(self, task_id: int, start=0) -> Task:
        if 0 <= task_id - start < len(self._tasks):
            return self._tasks[task_id - start]

        raise ValueError(f"Invalid task id: {task_id}")

    @property
    def description(self):
        return self._description

    def edit_task_description(self, task_id: int, new_description: str):
        task = self.get_task_by_id(task_id)
        task.description = new_description

    def set_task_status(self, task_id: int, new_status: str):
        task = self.get_task_by_id(task_id)
        task.status = new_status

    def filter_tasks_by_status(self, status: Optional[str]) -> list[Task]:
        if status is None:
            return self._tasks
        status = status.upper()
        tasks = []
        for task in self._tasks:
            if task.status == status:
                tasks.append(task)
        return tasks

    def __getitem__(self, item):
        return self._tasks[item]

    def __len__(self):
        return len(self._tasks)

    def __repr__(self):
        return "\n".join(map(str, self._tasks))

    def is_empty(self) -> bool:
        return len(self._tasks) == 0
