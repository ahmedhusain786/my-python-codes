# single level inheritence
class student:
    def __init__(self):
        self.rno= int(input("Enter roll number"))
        self.nm= input("Enter Name ")
        self.age= int(input("Enter age"))

    def putData(self):
        print("Roll Number :",self.rno)
        print("Name :",self.nm)
        print("Age :",self.age)
class result(student):
    def __init__(self):
        super().__init__()
        self.py = int(input("enter marks of python"))
        self.os = int(input("Enter marks for os"))
    def calc(self):
        self.total = self.py + self.os
        self.per= self.total/2
    def putData(self):
        super().putData()
        print("Total is ",self.total)
        print("Percentage is ",self.per)
r1 = result()
r1.calc()
r1.putData()