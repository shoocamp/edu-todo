import sys

from ToDo_CU import Task, main_storage


def main_menu():
    """printing of main menu & UI processing"""
    print('\n 1- add new task \n 2- edit description \n 3- edit status '
          f'\n 4- show active tasks \n 5- show all tasks ({len(main_storage.storage)}) '
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


def menu_for_choosing_tasks_to_change():   #  ахуенно было бы этой функцией предусмотреть все проверки, пустой лист
    #  и длину листа длина тут есть. надо добавить проверку на пустоту
    """printing of task list to choosing task & UI processing"""
    print('Choose task')
    print(main_storage.tasks_with_idexes())
    try:
        t_id = int(input())
        if t_id in range(len(main_storage.storage)+1):  # проверка дипазона достпных номеров задач
            return t_id
        else:
            print('Not exist')
            return menu_for_choosing_tasks_to_change()  # сама себя возвращает)
    except ValueError:
        print('You have to put only one digit from the list.')
        main_menu()


def is_list_empty():
    if len(main_storage.storage) == 0:
        print("List is empty yet. Put some tasks to start.")


while True:
    ui_main_menu = main_menu()

    if ui_main_menu == 1:
        task_description = input('Task description?\n')
        if task_description != "":
            task = Task(task_description)
            main_storage.add_task(task)
            print(main_storage.storage)
        else:
            print("Empty description is not allowed")

    elif ui_main_menu == 2:
        if len(main_storage.storage) != 0:  # проверка не пустой ли лист. не понимаю как избежать повторения
            # этих строк везде дальше...
            task_id = menu_for_choosing_tasks_to_change()
            new_description = input('New description:\n')
            main_storage.edit_description(task_id-1, new_description)
            print(f'Result is: {main_storage.storage[task_id-1]}\n'
                  f'And all list is:{main_storage.storage}')
        else:
            print("List is empty yet. Put some tasks to start.")
    elif ui_main_menu == 3:
        if len(main_storage.storage) != 0:
            task_id = menu_for_choosing_tasks_to_change()
            while True:
                try:
                    new_status = int(input("You can choose 1 - DONE or 2 - NEW status \n"))
                    break
                except ValueError:
                    print("Wrong input. Status should be int")
            if new_status == 1:
                main_storage.set_task_status(int(task_id) - 1, 'DONE')
                print(main_storage.tasks_with_idexes())
            elif new_status == 2:
                main_storage.set_task_status(int(task_id) - 1, 'NEW')
                print(main_storage.tasks_with_idexes())
            else:
                print(f"Unsupported status: {new_status}")
        else:
            print("List is empty yet. Put some tasks to start.")
    elif ui_main_menu == 4:
        main_storage.show_specific_list('new')

    elif ui_main_menu == 5:
        print(main_storage.storage)

    elif ui_main_menu == 6:
        main_storage.show_specific_list('done')
