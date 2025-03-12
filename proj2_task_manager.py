import os
import json
import re

USERS_FILE = "users.txt"

#User Authentication functions

#using regex for valid password

def is_valid_password(password):
    pattern = re.compile(
        r'^(?=.*[a-z])'   # at least one lowercase letter
        r'(?=.*[A-Z])'    # at least one uppercase letter
        r'(?=.*\d)'       # at least one digit
        r'(?=.*[@$!%*?&])'  # at least one special character
        r'[A-Za-z\d@$!%*?&]{8,}$'  # at least 8 characters
    )
    return bool(pattern.match(password))



# register new user
def reg_user():
    print("First time user? Please create your credentials")
    username = input("Enter a username: ").strip()
    password = input("Enter a password. Your password must contain  at least one lowercase letter, one uppercase letter, one number, one special character, and be at least 8 characters long. ").strip()
    if not is_valid_password(password):
        print("Invalid password.  It must have at least one lowercase letter, one uppercase letter, one number, one special character (@, $, !, %, *, ?, &), and be at least 8 characters long.")


    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            for line in file:
                stored_username, _ = line.strip().split(",")
                if stored_username == username:
                    print("Username already exists. Please try logging in or choose a different username.")
                    return None
    
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password}\n")
    
    print("User registered successfully!")
    return username

def login():
    print("Please log in.")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    if not os.path.exists(USERS_FILE):
        print("No registered users. Please register first.")
        return None
    
    with open(USERS_FILE, "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                print("Login successful!")
                return username
    print("Invalid credentials.")
    return None

#task managing functions

def load_tasks(username):
    filename = f"tasks_{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []
    return tasks

def save_tasks(username, tasks):
    filename = f"tasks_{username}.json"
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(username):
    tasks = load_tasks(username)
    description = input("Enter the task description: ").strip()
    task_id = max([task["id"] for task in tasks], default=0) + 1
    
    task = {
        "id": task_id,
        "description": description,
        "status": "Pending"
    }
    tasks.append(task)
    save_tasks(username, tasks)
    print(f"Task added successfully with ID {task_id}!")

def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
        return
    print("\n=== Your Tasks ===")
    for task in tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']}")
    print()

def mark_task_completed(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
        return
    try:
        task_id = int(input("Enter the task ID to mark as completed: "))
    except ValueError:
        print("Invalid input. Please enter a numeric task ID.")
        return
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            save_tasks(username, tasks)
            print("Task marked as completed!")
            return
    print("Task ID not found.")

def delete_task(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
        return
    try:
        task_id = int(input("Enter the task ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numeric task ID.")
        return
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task ID not found.")
    else:
        save_tasks(username, new_tasks)
        print("Task deleted successfully!")

print("Starting Task Manager")

def task_menu(username):
    while True:
        print("\n=== Task Manager Menu ===")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete a Task")
        print("5. Logout. Your tasks will be saved upon logout.")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

def main_menu():
    while True:
        print("\n=== Welcome to the Task Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            user = reg_user()
            if user:
                task_menu(user)
        elif choice == "2":
            user = login()
            if user:
                task_menu(user)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose between 1 and 3.")


if __name__ == "__main__":
    main_menu()         