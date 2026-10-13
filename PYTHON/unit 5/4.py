#access specifier
class student:
    def getData(self):
        self.rno= int(input("Enter roll no "))
        self._name= input("Enter Name ")
        self._semno= int(input("Enter Sem "))
    def putData(self):
        print("Rno is ",self.rno)
        print("Name is ",self._name)
        print("Sem is ",self._semno)
s1= student()
s1.rno=1
s1._name="Abc"
s1._semno=3
s1.getData()
s1.putData()