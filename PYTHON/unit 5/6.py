# access specifier another example
class ABC:
    def __init__(self):
        self.a=10
        self._b=20
        self.__c=30
    def putData(self):
        print(self.a)
        print(self._b)
        print(self.__c)
class XYZ(ABC):
    def showData(self):
        print("A is :",self.a)
        print("_B is :",self._b)

x1 = XYZ()
x1.showData()
print(x1.a)
print(x1._b)
print(x1.__c)
