# getdata and putdata and calcultate total and percentage also using constrcutor
class student:
    def __init__(self):

        print("Default Constructor Called")
    def getData(self):
        self.sid= int(input("Enter ID :"))
        self.snm= input("Enter Name :")
        self.python= int(input("Enter marks of python: "))
        self.dbms= int(input("Enter marks of dbms"))
    def calc(self):
        self.total = self.python + self.dbms
        self.per= self.total/2
    def putData(self):
        print("Student ID:",self.sid)
        print("Student Name:",self.snm)
        print("Total Marks :",self.total)
        print("Percentage :",self.per)
s1=student()
s1.getData()
s1.calc()
s1.putData()