class Employee:
    def __init__(self):
        self.eid = 0
        self.enm = "Abc"
        self.bs = 0
        self.hra = 0
        self.pf = 0
        self.net = 0
        print("Default Constructor Called")

    def getData(self):
        self.eid = int(input("Enter ID: "))
        self.enm = input("Enter Name: ")
        self.bs = float(input("Enter the basic salary: "))

    def calc(self):
        self.hra = self.bs * 0.20   # HRA = 20% of basic salary
        self.pf = self.bs * 0.12    # PF = 12% of basic salary
        self.net = self.bs + self.hra - self.pf

    def putData(self):
        print("\n--- Employee Details ---")
        print("Employee ID:", self.eid)
        print("Employee Name:", self.enm)
        print("Basic Salary:", self.bs)
        print("HRA:", self.hra)
        print("PF:", self.pf)
        print("Net Salary:", self.net)


e = Employee()
e.getData()
e.calc()
e.putData()