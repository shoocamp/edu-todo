import ToDo_CU


def print_list_with_indexes():
    """printing of list with indexes"""
    for (i, item) in enumerate(ToDo_CU.main_storage.storage, start=1):
        print(i, item)


def main_menu():
    """printing of main menu & UI processing"""
    print('\n 1- add new task \n 2- edit description \n 3- edit status '
          f'\n 4- show all tasks ({len(ToDo_CU.main_storage.storage)}) \n 5- show archive \n 6- show new tasks \n')
    try:
        ui = int(input())
        return ui
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


def checking_if_list_empty():
    if len(ToDo_CU.main_storage.storage) == 0:
        print("List is empty yet. Put some tasks to start.")


while True:
    ui_main_menu = main_menu()

    if ui_main_menu == 1:
        task_description = input('Task description?\n')
        task = ToDo_CU.Task(task_description)
        ToDo_CU.main_storage.add_task(task)
        print(ToDo_CU.main_storage.storage)

    elif ui_main_menu == 2:
        task_id = menu_for_choosing_tasks_to_change()
        new_description = input('New description:\n')
        ToDo_CU.main_storage.edit_description(task_id-1, new_description)
        print(f'Result is: {ToDo_CU.main_storage.storage[task_id-1]}\nAnd all list is:{ToDo_CU.main_storage.storage}')

    elif ui_main_menu == 3:
        print('Choose task')
        print_list_with_indexes()
        task_id = int(input())
        new_status = int(input("You can choose 1 - DONE or 2 - NEW status \n"))
        if new_status == 1:
            ToDo_CU.main_storage.set_status(task_id - 1, 'DONE')
            print_list_with_indexes()
        else:
            ToDo_CU.main_storage.set_status(task_id - 1, 'NEW')
            print_list_with_indexes()

    elif ui_main_menu == 4:
        checking_if_list_empty()
        print(ToDo_CU.main_storage.storage)

    elif ui_main_menu == 5:
        checking_if_list_empty()
        ToDo_CU.main_storage.show_specific_list('done')

    elif ui_main_menu == 6:
        checking_if_list_empty()
        ToDo_CU.main_storage.show_specific_list('new')
