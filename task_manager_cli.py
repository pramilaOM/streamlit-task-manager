import datetime
import os

def user_information(username, password):
    """Collects and saves user profile information to a text file."""
    name = input("Enter your full name: ")
    address = input("Enter your address: ")
    age = input("Enter your age: ")
    profile_file = username + "_profile.txt"
    task_file = username + "_tasks.txt"

    with open(profile_file, 'w') as f:
        f.write(password + '\n')
        f.write(f"Name: {name}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Age: {age}\n")

    # Initialize empty task file
    if not os.path.exists(task_file):
        with open(task_file, 'w') as f:
            f.write("")  # Empty task file


def signup():
    """Handles user signup and redirects to login."""
    print("\n--- SIGN UP ---")
    username = input("Choose a username: ")
    password = input("Create a password: ")
    user_information(username, password)
    print("Signup successful. Please proceed to login.\n")
    login()


def login():
    """Authenticates user login and presents options."""
    print("\n--- LOGIN ---")
    username = input("Enter your username: ")
    input_password = input("Enter your password: ") + '\n'
    profile_file = username + "_profile.txt"

    try:
        with open(profile_file, 'r') as f:
            saved_password = f.readline()
        
        if input_password == saved_password:
            print(f"\nWelcome, {username}!")

            while True:
                print("\nChoose an option:")
                print("1 - View Profile")
                print("2 - Add Task")
                print("3 - View All Tasks")
                print("4 - Update Task Status")
                print("5 - Delete Task")
                print("6 - Logout")

                choice = input("Enter your choice: ")

                if choice == '1':
                    view_profile(profile_file)
                elif choice == '2':
                    add_task(username)
                elif choice == '3':
                    view_tasks(username)
                elif choice == '4':
                    update_task_status(username)
                elif choice == '5':
                    delete_task(username)
                elif choice == '6':
                    print("Logged out.\n")
                    break
                else:
                    print("Invalid option. Try again.")
        else:
            print("Incorrect password.")
            login()

    except FileNotFoundError:
        print("User not found. Please sign up first.")
        signup()


def view_profile(profile_file):
    """Displays user's saved profile."""
    print("\n--- USER PROFILE ---")
    with open(profile_file, 'r') as file:
        print(file.read())


def add_task(username):
    """Adds a new task with a target date."""
    print("\n--- ADD TASK ---")
    task_file = username + "_tasks.txt"
    task = input("Enter Task Description: ")
    target = input("Enter Target Date (YYYY-MM-DD): ")
    status = "Not Started"
    task_id = str(int(datetime.datetime.now().timestamp()))  # Unique ID using timestamp

    with open(task_file, 'a') as f:
        f.write(f"{task_id}|{task}|{target}|{status}\n")
    print("Task added successfully!")


def view_tasks(username):
    """Displays all tasks with status."""
    print("\n--- YOUR TASKS ---")
    task_file = username + "_tasks.txt"

    try:
        with open(task_file, 'r') as f:
            tasks = f.readlines()
            if not tasks:
                print("No tasks found.")
                return
            for line in tasks:
                tid, task, target, status = line.strip().split('|')
                print(f"ID: {tid} | Task: {task} | Target: {target} | Status: {status}")
    except FileNotFoundError:
        print("No task file found.")


def update_task_status(username):
    """Updates status of a selected task."""
    task_file = username + "_tasks.txt"
    view_tasks(username)
    task_id = input("Enter the Task ID to update: ")
    new_status = input("Enter new status (Completed / Ongoing / Not Started): ")

    updated = False
    try:
        with open(task_file, 'r') as f:
            tasks = f.readlines()
        with open(task_file, 'w') as f:
            for line in tasks:
                tid, task, target, status = line.strip().split('|')
                if tid == task_id:
                    f.write(f"{tid}|{task}|{target}|{new_status}\n")
                    updated = True
                else:
                    f.write(line)
        if updated:
            print("Task status updated.")
        else:
            print("Task ID not found.")
    except FileNotFoundError:
        print("No task file found.")


def delete_task(username):
    """Deletes a selected task."""
    task_file = username + "_tasks.txt"
    view_tasks(username)
    task_id = input("Enter the Task ID to delete: ")

    deleted = False
    try:
        with open(task_file, 'r') as f:
            tasks = f.readlines()
        with open(task_file, 'w') as f:
            for line in tasks:
                tid, task, target, status = line.strip().split('|')
                if tid != task_id:
                    f.write(line)
                else:
                    deleted = True
        if deleted:
            print("Task deleted.")
        else:
            print("Task ID not found.")
    except FileNotFoundError:
        print("No task file found.")


if __name__ == '__main__':
    print("WELCOME TO TASK MANAGER")
    print("1 - Sign Up")
    print("0 - Log In")
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            signup()
        elif choice == 0:
            login()
        else:
            print("Invalid input. Please choose 1 or 0.")
    except ValueError:
        print("Please enter a valid number.")
