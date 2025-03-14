import os # for checking if file exists
import json # for storing key value pairs for tasks
import re # for using regex for stronger password

USERS_FILE = "users.txt" # initializes file to store usernames and passwords

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
    match = pattern.match(password)
    print(f"DEBUG: Password entered: '{password}' - Valid? {bool(match)}")
    return bool(match) # this is boolean return for password either matching regex criteria or not




# register new user
def reg_user():
    print("First time user? Please create your credentials")
    username = input("Enter a username: ").strip()
    # loop until the user enters valid password
    while True:
        password = input("Enter a password. Your password must contain  at least one lowercase letter, one uppercase letter, one number, one special character, and be at least 8 characters long. ").strip()
        if is_valid_password(password):
            break #exit loop if password is valid
        else:
            print("Invalid password.  It must have at least one lowercase letter, one uppercase letter, one number, one special character (@, $, !, %, *, ?, &), and be at least 8 characters long:")

# check if file already exists for the username by opening in "r" for read
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            for line in file:
                stored_username, _ = line.strip().split(",")
                if stored_username == username:
                    print("Username already exists. Please try logging in or choose a different username.")
                    return None
    # if the file exists, then open in "a" for append
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password}\n")
    
    print("User registered successfully!")
    return username

# defining login function
def login():
    print("Please log in.")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    # checking if the credentials do not exist already
    if not os.path.exists(USERS_FILE): 
        print("No registered users. Please register first.")
        return None
    # if credentials do exist, then open the file in "r" read mode then communicate to user that they are logged in now.  otherwise communicate that login failed
    with open(USERS_FILE, "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                print("Login successful!")
                return username
    print("Invalid credentials.")
    return None

#task managing functions---------------------------------
# defining the function to load tasks
def load_tasks(username):
    filename = f"tasks_{username}.json" #accessing only the tasks associated with username
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []
    return tasks
# defining the function to save tasks associated with username
def save_tasks(username, tasks):
    filename = f"tasks_{username}.json" # filename is the logged in username + .json
    if not tasks:
        print("No tasks to save.")
    else:    
        with open(filename, "w") as file: # opens the file whose name is stored in USERS_File in "w" mode so it will write to the file
            json.dump(tasks, file, indent=4) # converts the object so it can be stored into json type string with parameters
        print("Your tasks have been saved!")    
# defing the add task function
def add_task(username):
    tasks = load_tasks(username) # load the existing tasks so that when saving tasks, all of them are captured in the save
    description = input("Enter the task description: ").strip()
    task_id = max([task["id"] for task in tasks], default=0) + 1 # assing an id to the task but add 1 so the first in the index is 1 and not 0 which is more relatable to the user.
    # put the user input values for task in the json per the keys
    task = {
        "id": task_id,
        "description": description,
        "status": "Pending"
    }
    tasks.append(task) # add it to the tasks object
    save_tasks(username, tasks)
    print(f"Task added successfully with ID {task_id}!") # communicate back to user
# defining function to view tasks
def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
        return
    print("\n=== Your Tasks ===") # on a new line make a heading 
    for task in tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']}") # using f string to print the values beside the keys
    print()
# defining function to mark task completed
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
# defining function to delete a task
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

print("Starting Task Manager") # first thing to communicate to user once they start the program
# defining the task menu that user will see after they log in
def task_menu(username):
    while True:
        print("\n=== Task Manager Menu ===")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete a Task")
        print("5. Save Tasks")
        print("6. Logout. Your tasks will automatically be saved upon logout.")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            tasks = load_tasks(username)
            save_tasks(username, tasks)    
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
# defining first menu before user logs in
def main_menu():
    while True:
        print("\n=== Welcome to the Task Manager \U0001F600===")
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

# this code ensures that the function with "main" in the name runs first
if __name__ == "__main__":
    main_menu()         