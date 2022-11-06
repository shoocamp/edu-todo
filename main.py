todo_list = []


def add_tasks():
    while True:
        print('Add task N', str(len(todo_list) + 1), 'OR enter nothing to quit')
        new_task = input()
        if new_task == '':
            break
        todo_list.append(new_task)

    print('you`ve got', str(len(todo_list)), 'tasks in yor ToDo list. Here it is:', todo_list, '\n\n')


def remove_tasks():
    for t in range(len(todo_list)):
        print(todo_list[t], '-', str(t+1))
    print('which task you wanna kill? Or ENTER nothing to quit\n')
    num = input()
    if num == '':
        print('Ok, next time :)\n\n')
    else:
        num = int(num)
        del todo_list[num-1]
        print('Done. Here is new list', todo_list, '\n')


def showing_func():
    if len(todo_list) == 0:
        print('you have NOTHING to do, man\n\n')
    else:
        print(todo_list)


while True:
    print('Enter digit if you wonna:\n 1- see  list of tasks \n 2- add tasks \n 3- remove tasks \n 4- quit \n')
    digit = int(input())
    if digit == 1:
        showing_func()
    elif digit == 2:
        add_tasks()
    elif digit == 3:
        remove_tasks()
    elif digit == 4:
        print('see ya!')
        break
    elif digit >= 5 or digit < 0:
        print('That`s bullshit. Try again! \n')
