import os
import sys
from logic import add_task, list_tasks, toggle_task_status, delete_task, update_task

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n=== In-Memory Todo App ===")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Complete/Toggle Task")
    print("5. Delete Task")
    print("6. Exit")
    print("==========================")

def run_app():
    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title cannot be empty.")
                continue
            desc = input("Enter task description (optional): ").strip()
            add_task(title, desc)
            print("Task added successfully!")

        elif choice == '2':
            tasks = list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nYour Tasks:")
                for t in tasks:
                    print(f"[{t.id}] {t.title} - {t.status}")
                    if t.description:
                        print(f"    Description: {t.description}")

        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to update: "))
                new_title = input("Enter new title (leave blank to keep current): ").strip()
                new_desc = input("Enter new description (leave blank to keep current): ").strip()

                success = update_task(
                    task_id,
                    title=new_title if new_title else None,
                    description=new_desc if new_desc else None
                )
                if success:
                    print("Task updated successfully!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            except ValueError:
                print("Error: Please enter a valid numeric ID.")

        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to toggle: "))
                if toggle_task_status(task_id):
                    print("Task status toggled!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            except ValueError:
                print("Error: Please enter a valid numeric ID.")

        elif choice == '5':
            try:
                task_id = int(input("Enter task ID to delete: "))
                if delete_task(task_id):
                    print("Task deleted successfully!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            except ValueError:
                print("Error: Please enter a valid numeric ID.")

        elif choice == '6':
            print("Exiting. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid selection. Please choose 1-6.")

if __name__ == "__main__":
    run_app()
