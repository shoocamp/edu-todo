todo_list = []

while True:
    print('Put down your', str(len(todo_list) + 1), 'task you gonna do bro OR enter nothing to quit')
    new_task = input()
    if new_task == '':
        break
    todo_list = todo_list + [new_task]

print('you`ve got', str(len(todo_list)), 'tasks in yor ToDo list. Here it is:', todo_list)

