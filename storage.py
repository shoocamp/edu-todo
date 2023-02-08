import sqlite3
from datetime import datetime
from typing import Optional

from core import Task, TasksList
from users import User


class SQLiteStorage:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)

    def create_tasks_list(self, user_id, description) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO lists (description, user_id) VALUES ("{description}", {user_id})"""
        ).fetchall()
        self.con.commit()
        result = cur.execute("SELECT last_insert_rowid()").fetchone()
        return result[0]

    def get_tasks_for_list_id(self, user_id, list_id):
        result = self.con.cursor().execute(
            f"""SELECT * FROM tasks WHERE list_id={list_id} AND user_id={user_id}"""
        ).fetchall()
        return result

    def add_task(self, user_id, list_id, description, status, due_date=None) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""
            INSERT INTO tasks (description, status, created, due_date, notes, list_id, user_id)
                VALUES (
                "{description}",
                "{status}",
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
        # TODO: support all fields
        cur = self.con.cursor()
        cur.execute(
            f"""UPDATE tasks SET description="{description}" WHERE id={task_id}"""
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
            SELECT * FROM users WHERE id={user_id}
            """
        ).fetchone()
        return result

    def get_user_by_name(self, user_name: str):
        cur = self.con.cursor()
        result = cur.execute(
            f"""
            SELECT * FROM users WHERE name="{user_name}"
            """
        ).fetchone()
        return result

    def create_new_user(self, name, password_md5) -> int:
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO users (name, password_md5) VALUES ("{name}", "{password_md5}")"""
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


class TasksListBuilder:
    def __init__(self, storage: SQLiteStorage):
        self.storage = storage

    def build(self, user_id: int, list_id: int) -> TasksList:
        list_db_id, description, _ = self.storage.get_list(list_id)
        task_list = TasksList(description, storage=self.storage, db_id=list_db_id, user_id=user_id)
        related_tasks = self.storage.get_tasks_for_list_id(user_id, list_id)
        for task_db_id, description, status, created_ts, due_date_ts, _, _, _ in related_tasks:
            # TODO: proper init
            task = Task(description, storage=self.storage, db_id=task_db_id)
            task_list.add_task(task, save=False)

        return task_list


class UserBuilder:
    def __init__(self, storage: SQLiteStorage):
        self.storage = storage

    def build_by_id(self, user_id: int) -> User:
        user_id, user_name, _, default_list_id = self.storage.get_user(user_id)
        return User(user_id, user_name, default_list_id)

    def build_by_name(self, name: str) -> User:
        user_id, user_name, _, default_list_id = self.storage.get_user_by_name(name)
        return User(user_id, user_name, default_list_id)

    def build_new(self, username: str, password_md5: str) -> User:
        user_id = self.storage.create_new_user(username, password_md5)
        default_list_id = self.storage.create_tasks_list(user_id, "default")
        self.storage.set_user_default_list_id(user_id, default_list_id)
        return User(user_id, username, default_list_id)
