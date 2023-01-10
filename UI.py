import again


def print_list_with_indexes():  # printing of list with indexes
    for (i, item) in enumerate(again.main_storage.storage, start=1):
        print(i, item)


def main_menu():  # printing of main menu & UI processing
    print('\n 1- add new task \n 2- edit description \n 3- edit status '
          '\n 4- show all tasks \n 5- show archive \n 6- show new tasks \n')
    try:
        ui = int(input())
        return ui
    except ValueError:
        print('You have to put only one digit from the list below.')


def menu_for_choosing_tasks_to_change():  # printing of task list to choosing task & UI processing
    print('Choose task')
    print_list_with_indexes()
    try:
        t_id = int(input())
        return t_id
    except ValueError:
        print('You have to put only one digit from the list.')


while True:
    ui_main_menu = main_menu()

    if ui_main_menu == 1:
        task_description = input('Task description?\n')
        again.main_storage.add_task(task_description)
        print(again.main_storage.storage)

    elif ui_main_menu == 2:
        task_id = menu_for_choosing_tasks_to_change()
        new_description = input('New description:\n')
        again.main_storage.edit_description(task_id-1, new_description)
        print(f'Result is: {again.main_storage.storage[task_id-1]}\nAnd all list is:{again.main_storage.storage}')

    elif ui_main_menu == 3:
        print('Choose task')
        print_list_with_indexes()
        task_id = int(input())
        new_status = int(input("You can choose 1 - DONE or 2 - NEW status \n"))
        if new_status == 1:
            again.main_storage.set_status(task_id - 1, 'DONE')
            print_list_with_indexes()
        else:
            again.main_storage.set_status(task_id - 1, 'NEW')
            print_list_with_indexes()

    elif ui_main_menu == 4:
        print(again.main_storage.storage)

    elif ui_main_menu == 5:
        again.main_storage.show_specific_list('done')

    elif ui_main_menu == 6:
        again.main_storage.show_specific_list('new')
