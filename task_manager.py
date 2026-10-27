import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Warning: Invalid task data. Starting with an empty list.")
            return []

        return tasks

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading tasks: {error}")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

        return True

    except OSError as error:
        print(f"Error saving tasks: {error}")
        return False


def add_task(tasks):
    """Add a new task."""
    title = input("Enter task description: ").strip()

    if not title:
        print("Error: Task description cannot be empty.")
        return

    task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": title,
        "completed": False
    }

    tasks.append(task)

    if save_tasks(tasks):
        print("Task added successfully!")


def view_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n========== YOUR TASKS ==========")

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"

        print(
            f"ID: {task['id']} | "
            f"Task: {task['title']} | "
            f"Status: {status}"
        )

    print("================================")


def complete_task(tasks):
    """Mark a task as completed."""
    if not tasks:
        print("No tasks available to complete.")
        return

    try:
        task_id = int(input("Enter the task ID to complete: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print("This task is already completed.")
            else:
                task["completed"] = True

                if save_tasks(tasks):
                    print("Task marked as completed!")

            return

    print("Error: Task ID not found.")


def delete_task(tasks):
    """Delete a task by its ID."""
    if not tasks:
        print("No tasks available to delete.")
        return

    try:
        task_id = int(input("Enter the task ID to delete: "))

    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            if save_tasks(tasks):
                print("Task deleted successfully!")
            else:
                # Restore the task in memory if saving fails.
                tasks.append(task)

            return

    print("Error: Task ID not found.")
