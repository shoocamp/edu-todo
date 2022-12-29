# from OOP_ToDo import Tasks, List
#
# task_1 = Tasks("Lie")
# list_1 = List("Main_list")
#
# list_1.t_list.append(task_1)
# print(list_1)

# import datetime
#
# date = datetime.datetime.now()
#
# print(date.strftime("%H"))


class Task:
    """class represents conditions for task creations"""

    def __init__(self, dscr, lvl="low", due_date="March", status="new"):
        self.id = None
        self.dscr = dscr
        self.lvl = lvl
        self.due_date = due_date  # сюда надо подключить библиотеку чтобы делала + неделя от даты создания таска
        self.status = status

    def __repr__(self):
        return f"{self.dscr}"

class TaskList:
    def __init__(self, name):
        self.name = name
        self.tasks = {}
        self._counter = 0

    def add(self, task):
        self._counter += 1
        task.id = self._counter
        self.tasks[task.id] = task

    def delete(self, task_id):
        del self.tasks[task_id]

class Reminders(Task):
    pass  # день до дью дэйт


# можно дополнить отдельными элементами с напоминалкой! типа класс с наследованием

if __name__ == "__main__":
    tasks = TaskList('My first TODO list')

    task_1 = Task("Pup")
    task_2 = Task("Eat")
    task_3 = Task("Calm")
    tasks.add(task_1)
    tasks.add(task_2)
    tasks.add(task_3)
    print(tasks.tasks)

    tasks.delete(task_1.id)
    print(tasks.tasks)
