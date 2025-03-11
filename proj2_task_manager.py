import os
import json

USERS_FILE = "users.txt"

#User Authentication functions
def reg_user():
    print("First time user? Please create your credentials")
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()
    
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

