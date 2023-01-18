import sys

import ToDo_CU


def print_list_with_indexes():
    """printing of list with indexes"""
    for (i, item) in enumerate(ToDo_CU.main_storage.storage, start=1):
        print(i, item)


def main_menu():
    """printing of main menu & UI processing"""
    print('\n 1- add new task \n 2- edit description \n 3- edit status '
          f'\n 4- show active tasks \n 5- show all tasks ({len(ToDo_CU.main_storage.storage)}) '
          f'\n 6- show completed tasks  \n'
          ' OR Press Enter to Quit')
    ui = input()
    if ui == "":
        sys.exit(0)  # так можно? или это жесткое что-то?
    else:
        try:
            ui_dig = int(ui)
            return ui_dig
        except ValueError:
            print('You have to put only one digit from the list below.')


def menu_for_choosing_tasks_to_change():
    """printing of task list to choosing task & UI processing"""
    print('Choose task')
    print_list_with_indexes()
    try:
        t_id = int(input())
        return t_id
    except ValueError:
        print('You have to put only one digit from the list.')
        return "error"


def is_list_empty():
    if len(ToDo_CU.main_storage.storage) == 0:
        print("List is empty yet. Put some tasks to start.")


while True:
    ui_main_menu = main_menu()

    if ui_main_menu == 1:
        task_description = input('Task description?\n')
        if task_description != "":
            task = ToDo_CU.Task(task_description)
            ToDo_CU.main_storage.add_task(task)
            print(ToDo_CU.main_storage.storage)
        else:
            print("Empty description is not allowed")

    elif ui_main_menu == 2:
        if len(ToDo_CU.main_storage.storage) != 0:  # проверка не пустой ли лист. не понимаю как избежать повторения
            # этих строк везде дальше...
            task_id = menu_for_choosing_tasks_to_change()
            new_description = input('New description:\n')
            ToDo_CU.main_storage.edit_description(task_id-1, new_description)
            print(f'Result is: {ToDo_CU.main_storage.storage[task_id-1]}\n'
                  f'And all list is:{ToDo_CU.main_storage.storage}')
        else:
            print("List is empty yet. Put some tasks to start.")
    elif ui_main_menu == 3:
        if len(ToDo_CU.main_storage.storage) != 0:
            print('Choose task')
            print_list_with_indexes()
            task_id = input()
            if task_id != "":  # есть ли какой-то способ избегать этих if конструкций для проверки
                # введенных пользователем значений? дальше по коду если пользователь не введет цифру, то прога
                # завершится с ошибкой( опять IF городить?
                new_status = int(input("You can choose 1 - DONE or 2 - NEW status \n"))
                if new_status == 1:
                    ToDo_CU.main_storage.set_status(int(task_id) - 1, 'DONE')
                    print_list_with_indexes()
                else:
                    ToDo_CU.main_storage.set_status(int(task_id) - 1, 'NEW')
                    print_list_with_indexes()
            else:
                print("You didn`t pick a task")
        else:
            print("List is empty yet. Put some tasks to start.")

    elif ui_main_menu == 4:
        ToDo_CU.main_storage.show_specific_list('new')

    elif ui_main_menu == 5:
        print(ToDo_CU.main_storage.storage)

    elif ui_main_menu == 6:
        ToDo_CU.main_storage.show_specific_list('done')
