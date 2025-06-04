# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Melissa Zheng,6/5/2025,Completed full program per assignment spec
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


# Data Classes ------------------------------ #
class Person:
    """Stores the first and last name of a person"""
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value.isalpha():
            raise ValueError("First name must only contain letters.")
        self._first_name = value.strip().title()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value.isalpha():
            raise ValueError("Last name must only contain letters.")
        self._last_name = value.strip().title()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    """Stores a student and their course"""
    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        if len(value.strip()) == 0:
            raise ValueError("Course name cannot be empty.")
        self._course_name = value.strip().title()

    def __str__(self) -> str:
        return f"{super().__str__()} is enrolled in {self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """A collection of processing layer functions that work with Json files"""

    @staticmethod
    def read_data_from_file(file_name: str):
        """Reads data from a json file and returns a list of Student objects"""
        student_objects = []
        try:
            with open(file_name, "r") as file:
                json_students = json.load(file)
                for item in json_students:
                    student = Student(first_name=item["FirstName"],
                                      last_name=item["LastName"],
                                      course_name=item["CourseName"])
                    student_objects.append(student)
        except FileNotFoundError:
            student_objects = []  # file may not exist yet
        except Exception as e:
            IO.output_error_messages(message="Error reading from file.", error=e)
        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Writes a list of Student objects to a json file"""
        try:
            dict_list = [{"FirstName": s.first_name, "LastName": s.last_name, "CourseName": s.course_name}
                         for s in student_data]
            with open(file_name, "w") as file:
                json.dump(dict_list, file)
            IO.output_student_and_course_names(student_data)
        except Exception as e:
            IO.output_error_messages("Error: There was a problem writing to the file.", error=e)


# Presentation --------------------------------------- #
class IO:
    """A collection of presentation layer functions that manage user input and output"""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Displays custom error messages"""
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """Displays the menu of choices"""
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """Gets a menu choice from the user"""
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """Displays each student's full name and course"""
        print("-" * 50)
        for student in student_data:
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Prompts user to input student information and returns updated list"""
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            student = Student(first_name=student_first_name, last_name=student_last_name, course_name=course_name)
            student_data.append(student)
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the wrong type.", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body
students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
    elif menu_choice == "4":
        break
    else:
        print("Please only choose option 1, 2, 3, or 4.")

print("Program Ended")
