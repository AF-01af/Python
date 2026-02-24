import json
import os
from datetime import datetime, date
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class ToDo:
    #Attributes: tasks (list): A list to store tasks as dictionaries.
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def save_tasks(self):
        #Save current tasks to 'task.json'
        with open('task.json', 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        """
        Load tasks from 'task.json' if it exists.
        If the file is missing or corrupted, initialize an empty task list.
        """
        if os.path.exists('task.json'):
            try:
                with open('task.json', 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []

    # -------------------- Task Management --------------------
    def add_task(self, description, due_date, priority):
        """
        Add a new task to the list.

        Args:
            description (str): Task description.
            due_date (str): Task due date in 'MM-DD-YYYY' format.
            priority (str): Task priority ('high', 'medium', 'low').
        """
         #Assign a id
        max_id = max([t['id'] for t in self.tasks], default=0)
        task = {
            "id": max_id + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
            "due_date": due_date, # stored as string for JSON
            "priority": priority
        }
        self.tasks.append(task) 
        self.save_tasks()       
        print(f"{Fore.BLUE}✓ Task Added: {description}")

    def color_coded(self, task):
        """
        Determine the color for a task based on due date and priority.

        Args:
            task (dict): The task dictionary.

        Returns:
            str: A colorama Fore color code.
        """
        today = date.today()
        due_date_str = task.get("due_date")
        
        if not due_date_str:
            return Fore.WHITE # default if no due date
        
        try:
            # Convert string to date (MM-DD-YYYY format)
            due_date = datetime.strptime(due_date_str, '%m-%d-%Y').date()
            
            # Check if overdue
            if due_date < today:
                return Fore.RED
        except ValueError:
            pass  # Invalid date format, continue to priority check
        
        # Check priority
        priority = task.get("priority", "low").lower()
        if priority == "high":
            return Fore.LIGHTRED_EX
        elif priority == "medium":
            return Fore.YELLOW
        else:
            return Fore.GREEN  # low or default
            
    def view_task(self):
        """
        Display all tasks with proper coloring and status.
        Overdue tasks and high/medium priority tasks are highlighted.
        """
        print("\n" + "="*50)
        print(" "*15 + "YOUR TO-DO LIST")
        print("="*50)
        
        if not self.tasks:
            print("No tasks found. Your to-do list is empty!")
            return
            
        for task in self.tasks:
            color = self.color_coded(task)
            # Display main task info in color
            status = "✓" if task.get('completed') else "○"
            # Display metadata in normal color
            print(f"\n{color}{status} [{task['id']}] {task['description']}{Style.RESET_ALL}")
            print(f"  Priority: {task.get('priority', 'N/A').upper()}")
            print(f"  Due Date: {task.get('due_date', 'N/A')}")
            print(f"  Created: {task.get('created_at', 'N/A')}")
            
            if task.get('completed'):
                print(f"  Completed: {task.get('completed_at', 'N/A')}")

    def complete_task(self, task_id):
        """
        Mark a task as completed.

        Args:
            task_id (int): ID of the task to mark as completed.
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
                self.save_tasks()
                print(f"{Fore.GREEN}✓ Task Completed!")
                return 
        print(f"{Fore.RED}✗ Task not found")

    def delete_task(self, task_id):
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete.
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted = self.tasks.pop(i)
                self.save_tasks()
                print(f"{Fore.YELLOW}✓ Deleted: {deleted['description']}") 
                return 
        print(f"{Fore.RED}✗ Task not found")
        
    def clear_all_tasks(self):
        """Delete all tasks."""
        self.tasks = []
        self.save_tasks()
        print(f"{Fore.RED}✓ All tasks deleted!")

    def show_stats(self):
        """Display statistics about tasks: total, completed, pending, and completion rate."""

        total_task = len(self.tasks)
        completed = sum(1 for i in self.tasks if i["completed"])
        pending = total_task - completed
        completion_rate = (completed / total_task * 100) if total_task > 0 else 0
        
        print("\n" + "="*50)
        print(" "*18 + "STATISTICS")
        print("="*50)
        print(f"Total Tasks: {total_task} | Completed: {completed} | Pending: {pending}")
        print(f"Completion Rate: {completion_rate:.1f}%")
        #print("="*50)

# -------------------- Main Application Loop --------------------
def main():
    to_do = ToDo()
    
    while True:
        print("\n" + "="*50)
        print(" "*15 + "TO-DO LIST MANAGER")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Complete Task")
        print("5. Clear All Tasks")
        print("6. View Statistics")
        print("7. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            task_des = input("Enter task description: ").strip()
            if not task_des:
                print(f"{Fore.RED}✗ Description cannot be empty!")
                continue
                
            task_due_date = input("Due Date (MM-DD-YYYY): ").strip()
            
            try:
                # Validate date format
                datetime.strptime(task_due_date, "%m-%d-%Y")
                
                task_priority = input("Task priority (high/medium/low): ").strip().lower()
                
                if task_priority not in ["high", "medium", "low"]:
                    print(f"{Fore.RED}✗ Invalid priority. Using 'low' as default.")
                    task_priority = "low"
                
                to_do.add_task(task_des, task_due_date, task_priority)
                
            except ValueError:
                print(f"{Fore.RED}✗ Invalid date format. Task not added. Use MM-DD-YYYY")

        elif choice == "2":
            to_do.view_task()
            
        elif choice == "3":
            to_do.view_task()
            try:
                task_id = int(input("\nEnter task ID to delete: ").strip())
                to_do.delete_task(task_id)
            except ValueError:
                print(f"{Fore.RED}✗ Please enter a valid number!")
                
        elif choice == "4":
            to_do.view_task()
            try:
                task_id = int(input("\nEnter task ID to complete: ").strip())
                to_do.complete_task(task_id)
            except ValueError:
                print(f"{Fore.RED}✗ Please enter a valid number!")
                
        elif choice == "5":
            confirm = input("Are you sure? Type 'yes' to confirm: ").lower().strip()
            if confirm == "yes":
                to_do.clear_all_tasks()
            else:
                print(f"{Fore.BLUE}✓ Cancelled. No tasks were deleted.")
                
        elif choice == "6":
            to_do.show_stats()
            
        elif choice == "7":
            print(f"\n{Fore.CYAN}Goodbye! Stay productive! 🚀")
            break
            
        else: 
            print(f"{Fore.RED}✗ Invalid choice! Please enter 1-7.")


if __name__ == "__main__":
    main()