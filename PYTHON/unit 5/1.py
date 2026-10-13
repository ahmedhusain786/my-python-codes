# getdata and putdata using class
class Employee:
    def getData(self):
        self.eid= int(input("Enter ID :"))
        self.enm= input("Enter Name :")
    def putData(self):
        print(self.eid)
        print(self.enm)
e= Employee()
e.getData()
e.putData()