import datetime
class Task:
    """class represents conditions for task creations"""

    def __init__(self, description, lvl="low", due_date=datetime.date.today(), status="new"):
        self.id = None
        self.description = description
        self.lvl = lvl
        self.due_date = due_date  # сюда надо подключить библиотеку чтобы делала + неделя от даты создания таска
        self.status = status

    def __repr__(self):
        return f"{self.description}"

    def edit_description(self, new_description):
        self.description = new_description

    def edit_lvl(self, new_lvl):
        if new_lvl in ['mid', 'high', 'low']:
            self.lvl = new_lvl
        else:
            return "bull shit"

    def edit_due_date(self, new_date):
        self.due_date = new_date

    def edit_status(self, new_status):
        if new_status in ['new', 'done']:
            self.status = new_status
        else:
            return "Only two options available"


class Lists:
    def __init__(self, list_description=""):
        self.list_description = list_description
        self.bank = []

    def add(self, task):
        self.bank.append(task)

    def show_new(self, only_new):
        only_new.bank.clear()
        for t in self.bank:
            if t.__dict__['status'] == 'new':
                only_new.bank.append(t)
            else:
                continue

    def show_archive(self, only_done):
        only_done.bank.clear()
        for t in self.bank:
            if t.__dict__['status'] == 'done':
                only_done.bank.append(t)
            else:
                continue




tasks = Lists("All_tasks")
new_tasks = Lists("New_tasks")
archive = Lists("Archive")

if __name__ == "__main__":
    # tasks = TaskList('My first TODO list')

    task_1 = Task("Pup")
    task_2 = Task("Eat")
    task_3 = Task("Calm")
    task_4 = Task("Lube")
    task_5 = Task("Stand")

    tasks.add(task_5)
    tasks.add(task_4)
    tasks.add(task_3)
    tasks.add(task_2)
    tasks.add(task_1)



    task_1.edit_status('done')
    task_2.edit_status('done')
    task_3.edit_status('done')


    print(tasks.bank)











