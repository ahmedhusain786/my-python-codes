class Student:
    def __init__(self):
        self.rno= 1
        self.nm="Abc"
    def getData(self):
        self.rno=int(input("Enter Roll No :"))
        self.nm = input("Enter Name :")
    def putData(self):
        print("Roll No is :",self.rno)
        print("Name is :",self.nm)
class Internal(Student):
    def __init__(self):
        self.itotal=200
    def getData(self):
        super().getData()
        self.itotal=int(input("Enter Internal Marks :"))
    def putData(self):
        super().putData()
        print("Total Internal Marks is :",self.itotal)
class External(Internal):
    def __init__(self):
        self.etotal=200
    def getData(self):
        super().getData()
        self.etotal=int(input("Enter external Marks :"))
    def putData(self):
        super().putData()
        print("Total external Marks is :",self.etotal)
e1=External()
e1.getData()
e1.putData()