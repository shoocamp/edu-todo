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


    def add_task(self, descriprion):
        task = Task(descriprion)
        self.storage.append(task)
        print(f'task "{descriprion}" added')


    def set_status(self, task_id, new_status):
        task = self.storage[task_id]
        task.status = new_status
        print(f'status of "{task.description}" replaced by {new_status}')

    def show_specific_list(self, specific_status):
        for task in self.storage:
            if task.status == specific_status:
                print(f"{specific_status} tasks here: {task.description} : {task.status}")


main_base = Base('Main base')

main_base.add_task('lup')
main_base.add_task('pupa')
main_base.add_task('zukko')
main_base.add_task('pipika')
main_base.add_task('hophopa')
main_base.add_task('zhuzhuzhu')

print(main_base.storage)  # checking whole the list

main_base.set_status(2, "done")        # test editing task status
main_base.set_status(4, "done")

print(main_base.storage)  # checking whole the list whith changes

main_base.show_specific_list("done")                # checking how functions work
# show_archive()