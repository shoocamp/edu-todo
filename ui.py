import sys
from rich.prompt import IntPrompt
from todo_cu import Task, main_storage
from datetime import datetime as dt


def validatetime(date_time_text):  # нашел такую функцию на стековерфло. это ж не запрещено?)
    try:
        due_date = dt.strptime(date_time_text, '%Y-%m-%d, %H:%M')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD, H:M")
    return due_date


def menu_of_tasks_to_change():
    """printing of task list to choosing task & UI processing"""
    print(main_storage.tasks_with_idexes())
    choices = []
    for t in range(int(len(main_storage.storage))):
        choices.append(str(t + 1))
    ui = IntPrompt.ask('Pick a task \n', choices=choices, show_choices=False)
    return ui


class CLIHandler:
    def __init__(self, storage_param):
        self.storage_param = storage_param

    def create_task(self):
        task_description = input('Task description?\n')
        if task_description != "":
            task = Task(task_description)
            self.storage_param.add_task(task)
            print(self.storage_param.storage)
        else:
            print("Empty description is not allowed")
        due_date = input('Set due date.\nFormat, should be YYYY-MM-DD, H:M\n')
        try:
            validatetime(due_date)
            task.due_date = due_date
        except ValueError:
            print("cheto s datoi")

    def edit_description(self):
        if self.storage_param.is_list_empty():
            print("List is empty yet")
        else:
            task_id = menu_of_tasks_to_change()
            new_description = input('New description:\n')
            if new_description != "":
                self.storage_param.edit_description(task_id - 1, new_description)
                print(f'Result is: {self.storage_param.storage[task_id - 1]}\n'
                      f'And all list is:{self.storage_param.storage}')
            else:
                print("Empty description is not allowed")

    def edit_status(self):
        if self.storage_param.is_list_empty():
            print("List is empty yet")
        else:
            print("taak")
            task_id = menu_of_tasks_to_change()
            new_status = IntPrompt.ask('You can choose 1 - DONE or 2 - NEW status \n', choices=["1", "2"])
            if new_status == 1:
                self.storage_param.set_task_status(int(task_id) - 1, 'DONE')
                print(self.storage_param.tasks_with_idexes())
            else:
                self.storage_param.set_task_status(int(task_id) - 1, 'NEW')
                print(self.storage_param.tasks_with_idexes())

    def show_with_status(self, specific):
        if specific == '':
            print(self.storage_param.storage)
        else:
            self.storage_param.show_specific_list(specific)


def main_menu():
    """main menu"""
    ui = IntPrompt.ask('\n 1- add new task \n 2- edit description \n 3- edit status '
                       f'\n 4- show active tasks \n 5- show all tasks ({len(main_storage.storage)}) '
                       f'\n 6- show completed tasks  \n'
                       ' 7- Quit \n', choices=["1", "2", "3", "4", "5", "6", "7"],
                       show_choices=False)
    if ui == 7:
        sys.exit(0)
    else:
        return ui


handler = CLIHandler(main_storage)

while True:
    ui_main_menu = main_menu()

    if ui_main_menu == 1:
        handler.create_task()

    elif ui_main_menu == 2:
        handler.edit_description()

    elif ui_main_menu == 3:
        handler.edit_status()

    elif ui_main_menu == 4:
        handler.show_with_status('new')

    elif ui_main_menu == 5:
        handler.show_with_status('')

    elif ui_main_menu == 6:
        handler.show_with_status('done')
