import csv
import re
import getpass

class User:
    def __init__(self, firstname, lastname, email, password, egyptian_number):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.egyptian_number = egyptian_number

class Project:
    def __init__(self, title, target, details, start_date, end_date):
        self.title = title
        self.target = target
        self.details = details
        self.start_date = start_date
        self.end_date = end_date

class Project_Data:
    def __init__(self):
        self.users = []
        self.projects = []

    def load_users(self, users_file):
        with open(users_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(row['firstname'], row['lastname'], row['email'], row['password'], row['egyptian_number'])
                self.users.append(user)

    def load_projects(self, projects_file):
        with open(projects_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                project = Project(row['title'], row['target'], row['details'], row['start_date'], row['end_date'])
                self.projects.append(project)

    # def validate_egyptian_number(self, egyptian_number):
    #     # Validate the Egyptian number (example validation)
    #     if re.match(r'^[0-9]{11}$', egyptian_number):
    #         return True
    #     else:
    #         return False

    def authenticate(self):
        while True:
            print("Welcome! Choose an option:")
            print("1. Register")
            print("2. Log in")
            print("3. Quit")
            choice = input()

            if choice == '1':
                self.register()
            elif choice == '2':
                user = self.login()
                if user:
                    self.main_menu(user)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def register(self):
     while True:  # Add a loop to allow re-entry tol ma kollo sah
        firstname = input("Enter your first name: ")
        if not firstname.isalpha():
            print("Invalid first name. First name should contain only alphabetic characters.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  # Exit the registration process and return to the next caller
            continue  # Restart the loop ll hta de 


        lastname = input("Enter your last name: ")
        if not lastname.isalpha():
            print("Invalid last name. Last name should contain only alphabetic characters.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  
            continue  

        email = input("Enter your email: ")
        # email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("Invalid email format.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  
            continue  

        # Check if the email is already registered and not unique 
        if any(user.email == email for user in self.users):
            print("Email already exists. Please choose a different one.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  
            continue  

        password = getpass.getpass("Enter a password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  
            continue  
           

        egyptian_number = input("Enter your Egyptian number: ")
        # Egyptian Number Validation 
        if not re.match(r'^01\d{9}$', egyptian_number):
            print("Invalid Egyptian number format.")
            choice = input("Press 'E' to exit or any other key to try again: ")
            if choice.lower() == 'e':
                return  
            continue  
            
        
        user = User(firstname, lastname, email, password, egyptian_number)
        self.users.append(user)
        print("Registration successful!")
        break 


    def login(self):
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        for user in self.users:
            if user.email == email and user.password == password:
                print("Login successful!")
                return user
        print("Login failed. Please check your email and password.")
        return None

    def main_menu(self, user):
        while True:
            print(f"Welcome, {user.firstname} {user.lastname}! Choose an option:")
            print("1. Create a new project")
            print("2. View all projects")
            print("3. Edit a project")
            print("4. Delete a project")
            print("5. Search for a project by date")
            print("6. Log out")
            choice = input()

            if choice == '1':
                self.create_project()
            elif choice == '2':
                self.view_projects()
            elif choice == '3':
                self.edit_project()
            elif choice == '4':
                self.delete_project()
            elif choice == '5':
                self.search_project_by_date()
            elif choice == '6':
                print("Logging out. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_project(self):
        title = input("Enter project title: ")

        # target amount validation
        while True:
            target = input("Enter project target amount: ")
            if not target.isdigit(): ## checks if a string is a number ,, "3" not 3 
                print("Invalid target amount. Please enter a valid number.")
                continue
            target = int(target)
            break

        details = input("Enter project details: ")

       
        while True:
            start_date = input("Enter project start date (YYYY-MM-DD): ")
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', start_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            break

        
        while True:
            end_date = input("Enter project end date (YYYY-MM-DD): ")
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', end_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            if end_date < start_date:
                print("End date cannot be earlier than the start date.")
                continue
            break

        project = Project(title, target, details, start_date, end_date)
        self.projects.append(project)
        print("Project created successfully!")


    def view_projects(self):
        print("All projects:")
        for idx, project in enumerate(self.projects, start=1):
            print(f"{idx}. Title: {project.title}, Start Date: {project.start_date}, End Date: {project.end_date}")

    def edit_project(self):
        self.view_projects()
        project_idx = int(input("Enter the project number to edit: ")) - 1
        if 0 <= project_idx < len(self.projects):
            new_title = input("Enter the new project title: ")
            new_start_date = input("Enter the new project start date (YYYY-MM-DD): ")
            new_end_date = input("Enter the new project end date (YYYY-MM-DD): ")
            self.projects[project_idx].title = new_title
            self.projects[project_idx].start_date = new_start_date
            self.projects[project_idx].end_date = new_end_date
            print("Project edited successfully!")
        else:
            print("Invalid project number.")

    def delete_project(self):
        self.view_projects()
        project_idx = int(input("Enter the project number to delete: ")) - 1
        if 0 <= project_idx < len(self.projects):
            del self.projects[project_idx]
            print("Project deleted successfully!")
        else:
            print("Invalid project number.")

    def search_project_by_date(self):
        search_date = input("Enter the date to search for (e.g., '2023-09-23'): ")
        matching_projects = [project for project in self.projects if project.start_date <= search_date <= project.end_date]
        if matching_projects:
            print("Matching projects:")
            for project in matching_projects:
                print(f"Title: {project.title}, Start Date: {project.start_date}, End Date: {project.end_date}")
        else:
            print("No projects found for the specified date.")

if __name__ == "__main__":
    app = Project_Data()
    users_file = "users.csv"
    projects_file = "projects.csv"

    # Load user and project data from CSV files
    app.load_users(users_file)
    app.load_projects(projects_file)

    app.authenticate()

