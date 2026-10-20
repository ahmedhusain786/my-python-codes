class Person:
    def show_person(self):
        print("I am a Person")


# Multilevel Inheritance
class Student(Person):
    def show_student(self):
        print("I am a Student")


class Result(Student):
    def show_result(self):
        print("I have a Result")


# Hierarchical Inheritance
class Teacher(Person):
    def show_teacher(self):
        print("I am a Teacher")


# Hybrid Inheritance
class Sports(Result, Teacher):
    def show_sports(self):
        print("I play Sports")


# Main Program
obj = Sports()

obj.show_person()
obj.show_student()
obj.show_result()
obj.show_teacher()
obj.show_sports()