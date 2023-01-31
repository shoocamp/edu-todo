import sys
from rich.prompt import IntPrompt, Confirm, Prompt
from todo_cu import Task, get_default_storage
from datetime import datetime as dt


class CLIHandler:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create_task(self):
        task_description = Prompt.ask('Task description')
        task = Task(description=task_description)

        if Confirm.ask("Add due date?", default=False):
            due_date = Prompt.ask('Set due date (format YYYY-MM-DD, H:M)')
            task.due_date = dt.strptime(due_date, '%Y-%m-%d, %H:%M')

        self.task_storage.add_task(task)

    def edit_description(self):
        task_id = self.get_task_id()
        new_description = Prompt.ask('New description')
        self.task_storage.edit_description(task_id, new_description)
        print("Done")

    def edit_status(self):
        task_id = self.get_task_id()
        status_id = IntPrompt.ask('You can choose 1 - DONE or 2 - NEW status', choices=["1", "2"])

        status_mapping = {
            1: "DONE",
            2: "NEW"
        }

        self.task_storage.set_task_status(task_id, status_mapping[status_id])

    def show_with_status(self, status, indexes=False):
        lines = []
        for i, t in enumerate(self.task_storage.filter_tasks_by_status(status), start=1):
            due_date = t.due_date.strftime("%d.%m.%y - %H.%M") if t.due_date is not None else ""
            status = "☐" if t.status == "NEW" else "☑"

            if indexes:
                lines.append(f"{i} - {status} {t.description}\t{due_date}")
            else:
                lines.append(f"{status} {t.description}\t{due_date}")

        print("\n".join(lines))

    def get_main_menu_command(self):
        """main menu"""
        options = [
            "Commands:\n"
            "1: add new task",
            "2: edit description",
            "3: edit status",
            "4: show active tasks",
            f"5: show all tasks ({self.task_storage.get_size()})",
            "6: show completed tasks",
            "7: quit\n"
        ]
        command = IntPrompt.ask("\n".join(options), choices=["1", "2", "3", "4", "5", "6", "7"],
                                show_choices=False)
        return command

    def get_task_id(self):
        """printing of task list to choosing task & UI processing"""
        self.show_with_status(None, indexes=True)
        choices = []
        for t in range(int(len(self.task_storage.storage))):
            choices.append(str(t + 1))
        task_id = IntPrompt.ask('Pick a task \n', choices=choices, show_choices=False)
        return task_id - 1


if __name__ == "__main__":
    handler = CLIHandler(get_default_storage())

    while True:
        main_menu_command = handler.get_main_menu_command()

        try:
            if main_menu_command == 1:
                handler.create_task()
            elif main_menu_command == 2:
                handler.edit_description()
            elif main_menu_command == 3:
                handler.edit_status()
            elif main_menu_command == 4:
                handler.show_with_status('new')
            elif main_menu_command == 5:
                handler.show_with_status(None)
            elif main_menu_command == 6:
                handler.show_with_status('done')
            elif main_menu_command == 7:
                print("bye")
                sys.exit(0)
        except KeyboardInterrupt:
            # `ctrl + c` - exit from sub-menu
            print(f"\nUndo cmd {main_menu_command}")
            continue
        except Exception as e:
            print(e)
