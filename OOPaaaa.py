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


class Tasks:
    """class represents conditions for task creations"""
    def __init__(self, dscr, lvl="low", due_date="March", status="new"):
        self.dscr = dscr
        self.lvl = lvl
        self.due_date = due_date    #сюда надо подключить библиотеку чтобы делала + неделя от даты создания таска
        self.status = status

    def __repr__(self):
       return f"{self.dscr}"


class Dict:
    """class represents list description"""
    def __init__(self, name):
        self.name = name
        self.t_dict = {}

    def add_task(self, name):
        self.t_dict[name] = (name.lvl, name.status, name.due_date)
        pass

    # def __delitem__(self, key):  я так понял надо в сторону этой этого мэджик метода смотреть??
    #     del self[key]
    def del_task(self, task):
        del self[task.dscr]
        pass

    def showALL_tasks(self):
        pass

    def __repr__(self):
       return f"{self.t_dict}"

class Reminders(Tasks):
    pass          #день до дью дэйт

# можно дополнить отдельными элементами с напоминалкой! типа класс с наследованием

if __name__=="__main__":

    dict_1 = Dict("Work list")

    task_1 = Tasks("Pup")
    task_2 = Tasks("Eat")
    task_3 = Tasks("Calm")
    dict_1.add_task(task_1)
    dict_1.add_task(task_2)
    dict_1.add_task(task_3)
    print(dict_1)

    dict_1.del_task(task_1)



    print(dict_1)



