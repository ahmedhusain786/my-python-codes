class Employee:

    def __init__(self, eid=0, ename="", esal=0):
        self.empid = eid
        self.empname = ename
        self.basicsal = esal
        self.hrf = 0
        self.da = 0
        self.pf = 0
        self.netsal = 0

    def getData(self):
        self.empid = int(input("Enter Employee ID: "))
        self.empname = input("Enter Employee Name: ")
        self.basicsal = float(input("Enter Basic Salary: "))

    def calcsalary(self):
        self.hrf = self.basicsal * 10 / 100
        self.da = self.basicsal * 20 / 100
        self.pf = self.basicsal * 12 / 100
        self.netsal = self.basicsal + self.hrf + self.da - self.pf

    def putdata(self):
        print("\nEmployee Details")
        print("Employee ID:", self.empid)
        print("Employee Name:", self.empname)
        print("Basic Salary:", self.basicsal)
        print("HRF:", self.hrf)
        print("DA:", self.da)
        print("PF:", self.pf)
        print("Net Salary:", self.netsal)
        print("============================")


# Parameterized Constructor
e1 = Employee(102, "Rahul", 30000)
e1.calcsalary()
e1.putdata()


# Multiple Employees using Default Constructor
employee = []

for i in range(2):
    s1 = Employee()
    s1.getData()
    s1.calcsalary()
    employee.append(s1)


# Display all employees
for i in range(2):
    employee[i].putdata()