class Emp:

    def __init__(self, eid=0, ename="", esal=0):
        self.eid = eid
        self.enm = ename
        self.bs = esal
        self.hrf = 0
        self.da = 0
        self.pf = 0
        self.netsal = 0

    def getData(self):
        self.eid = int(input("Enter Employee ID: "))
        self.enm = input("Enter Employee Name: ")
        self.bs = float(input("Enter Basic Salary: "))

    def calcsalary(self):
        self.hrf = self.bs * 10 / 100
        self.da = self.bs * 20 / 100
        self.pf = self.bs * 12 / 100
        self.netsal = self.bs + self.hrf + self.da - self.pf

    def putdata(self):
        print("\nEmployee Details")
        print("Employee ID:", self.eid)
        print("Employee Name:", self.enm)
        print("Basic Salary:", self.bs)
        print("HRF:", self.hrf)
        print("DA:", self.da)
        print("PF:", self.pf)
        print("Net Salary:", self.netsal)
        print("============================")