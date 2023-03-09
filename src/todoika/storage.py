import sqlite3
import psycopg2
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from todoika.core import TasksList
from todoika.users import User
from config import host, user, password, db_name, port


class Storage(ABC):

    @abstractmethod
    def create_tasks_list(self, user_id, description) -> int:
        ...

    @abstractmethod
    def get_tasks_for_list_id(self, list_id):
        ...

    @abstractmethod
    def update_task(self,
                    task_id: int,
                    description: Optional[str] = None,
                    status: Optional[str] = None,
                    due_date: Optional[datetime] = None):
        ...

    @abstractmethod
    def add_task(self, user_id, list_id, description, status, due_date=None) -> int:
        ...

    @abstractmethod
    def get_list(self, tasks_list_id):
        ...

    @abstractmethod
    def get_user(self, user_id):
        ...

    @abstractmethod
    def get_user_by_name(self, user_name: str):
        ...

    @abstractmethod
    def create_new_user(self, name, password_md5) -> int:
        ...

    @abstractmethod
    def set_user_default_list_id(self, user_id, list_id):
        ...

    @abstractmethod
    def get_task_by_id(self, task_id: int):
        ...


class SQLiteStorage(Storage):
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)

    def create_tasks_list(self, user_id, description) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO lists (description, user_id) VALUES ('{description}', {user_id})"""
        ).fetchall()
        self.con.commit()
        result = cur.execute("SELECT last_insert_rowid()").fetchone()
        return result[0]

    def get_tasks_for_list_id(self, list_id):
        result = self.con.cursor().execute(
            f"""SELECT * FROM tasks WHERE list_id={list_id}"""
        ).fetchall()
        return result

    def add_task(self, user_id, list_id, description, status, due_date=None) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""
            INSERT INTO tasks (description, status, created, due_date, notes, list_id, user_id)
                VALUES (
                '{description}',
                '{status}',
                {int(datetime.now().timestamp())},
                {int(due_date.timestamp()) if due_date is not None else 'null'},
                null,
                {list_id},
                {user_id})
             """).fetchall()
        self.con.commit()
        result = cur.execute("SELECT last_insert_rowid()").fetchone()
        return result[0]

    def update_task(self,
                    task_id: int,
                    description: Optional[str] = None,
                    status: Optional[str] = None,
                    due_date: Optional[datetime] = None):

        cur = self.con.cursor()
        if description:
            cur.execute(
                f"""UPDATE tasks SET description='{description}' WHERE id={task_id}"""
            ).fetchall()
        if status:
            cur.execute(
                f"""UPDATE tasks SET status='{status}' WHERE id={task_id}"""
            ).fetchall()
        if due_date:
            cur.execute(
                f"""UPDATE tasks SET due_date='{due_date.timestamp()}' WHERE id={task_id}"""
            ).fetchall()

        self.con.commit()

    def get_list(self, tasks_list_id):
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT * FROM lists WHERE id={tasks_list_id}
            """
        ).fetchone()
        return result

    def get_user(self, user_id):
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT id, name, default_list FROM users WHERE id={user_id}
            """
        ).fetchone()
        return result

    def get_user_by_name(self, user_name: str):
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT * FROM users WHERE name='{user_name}'
            """
        ).fetchone()
        return result

    def get_password_by_name(self, user_name: str):
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT password_md5 FROM users WHERE name='{user_name}'
            """
        ).fetchone()
        return result[0]

    def create_new_user(self, name, password_md5) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO users (name, password_md5) VALUES ('{name}', '{password_md5}')"""
        ).fetchall()
        self.con.commit()
        result = cur.execute("SELECT last_insert_rowid()").fetchone()
        return result[0]

    def set_user_default_list_id(self, user_id, list_id):
        cur = self.con.cursor()
        cur.execute(
            f"""UPDATE users SET default_list={list_id} WHERE id={user_id}"""
        ).fetchall()
        self.con.commit()

    def get_task_by_id(self, task_id: int) -> tuple:
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT * FROM tasks WHERE id={task_id}
            """
        ).fetchone()
        return result


class PSQLStorage(Storage):
    def __init__(self):
        self.con = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )

    def create_tasks_list(self, user_id, description) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO lists (description, user_id) VALUES ('{description}', {user_id}) RETURNING id"""
        )
        self.con.commit()
        return cur.fetchone()[0]

    def get_tasks_for_list_id(self, list_id):
        cur = self.con.cursor()
        cur.execute(
            f"""SELECT * FROM tasks WHERE list_id={list_id}"""
        )
        result = cur.fetchall()
        return result

    def add_task(self, user_id, list_id, description, status, due_date=None) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""
            INSERT INTO tasks (description, status, created, due_date, notes, list_id, user_id)
                VALUES (
                '{description}',
                '{status}',
                {int(datetime.now().timestamp())},
                {int(due_date.timestamp()) if due_date is not None else 'null'},
                null,
                {list_id},
                {user_id})
                RETURNING id
             """)
        self.con.commit()
        return cur.fetchone()[0]

    def update_task(self,
                    task_id: int,
                    description: Optional[str] = None,
                    status: Optional[str] = None,
                    due_date: Optional[datetime] = None):
        cur = self.con.cursor()
        if description:
            cur.execute(
                f"""UPDATE tasks SET description='{description}' WHERE id={task_id}"""
            )
        if status:
            cur.execute(
                f"""UPDATE tasks SET status='{status}' WHERE id={task_id}"""
            )
        if due_date:
            cur.execute(
                f"""UPDATE tasks SET due_date='{due_date.timestamp()}' WHERE id={task_id}"""
            )
        self.con.commit()

    def get_list(self, tasks_list_id):
        cur = self.con.cursor()
        cur.execute(
            f"""
            SELECT * FROM lists WHERE id={tasks_list_id}
            """
        )
        result = cur.fetchone()
        return result

    def get_user(self, user_id):
        cur = self.con.cursor()
        cur.execute(
            f"""
            SELECT id, name, default_list FROM users WHERE id={user_id}
            """
        )
        result = cur.fetchone()
        return result

    def get_user_by_name(self, user_name: str):
        cur = self.con.cursor()
        cur.execute(
            f"""
            SELECT * FROM users WHERE name='{user_name}'
            """
        )
        result = cur.fetchone()
        return result

    def get_password_by_name(self, user_name: str):
        cur = self.con.cursor()
        cur.execute(
            f"""
            SELECT password_md5 FROM users WHERE name='{user_name}'
            """
        )
        result = cur.fetchone()
        return result[0]

    def create_new_user(self, name, password_md5) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO users (name, password_md5) VALUES ('{name}', '{password_md5}') RETURNING id"""
        )
        self.con.commit()
        return cur.fetchone()[0]

    def set_user_default_list_id(self, user_id, list_id):
        cur = self.con.cursor()
        cur.execute(
            f"""UPDATE users SET default_list={list_id} WHERE id={user_id}"""
        )
        self.con.commit()

    def get_task_by_id(self, task_id: int) -> tuple:
        cur = self.con.cursor()
        cur.execute(
            f"""
            SELECT * FROM tasks WHERE id={task_id}
            """
        )
        result = cur.fetchone()
        return result


class TasksListBuilder:
    def __init__(self, storage: PSQLStorage):
        self.__storage = storage

    def build(self, user_id: int, list_id: int) -> TasksList:
        list_db_id, description, _ = self.__storage.get_list(list_id)
        related_tasks = self.__storage.get_tasks_for_list_id(list_id)
        return TasksList.from_db(description, self.__storage, list_db_id, user_id, related_tasks)


class UserBuilder:
    def __init__(self, storage: PSQLStorage):
        self.__storage = storage

    def build_by_id(self, user_id: int) -> User:
        user_id, user_name, default_list_id = self.__storage.get_user(user_id)
        return User(user_id, user_name, default_list_id)

    def build_by_name(self, name: str) -> User:
        user_id, user_name, _, default_list_id = self.__storage.get_user_by_name(name)
        return User(user_id, user_name, default_list_id)

    def build_new(self, username: str, password_md5: str) -> User:
        user_id = self.__storage.create_new_user(username, password_md5)
        default_list_id = self.__storage.create_tasks_list(user_id, "default")
        self.__storage.set_user_default_list_id(user_id, default_list_id)
        return User(user_id, username, default_list_id)
