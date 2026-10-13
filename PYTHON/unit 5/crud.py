lstemp=[]
import Employee
while True:
    print("=================EMPLOYEE CRUD===================================================")
    print("1.Add Employee\n2.Display Employee\n3.Search Employee\n4.Update\n5.Delete\n6.Exit")
    print("=================================================================================")
    ch = int(input("Enter your choice :"))
    if ch==1:
        emp= Employee.Emp()
        emp.getData()
        found = False
        for e in lstemp:
            if e.eid==emp.eid:
                found = True
                break
        if found:
            print("Employee ID already exist")
        else:
            emp.calcsalary()
            lstemp.append(emp)
    elif ch == 2:
        if len(lstemp)==0:
            print("No data found")
        else:
            for e in lstemp:
                e.putdata()
    elif ch == 3:
        key= input("Enter ID or Name to Search")
        found = 0
        for e in lstemp:
            if e.eid or e.enm == key:
                found = 1
                break
        if found == 1:
            e.putdata()
        else:
            print("No data found")
    elif ch==4:
        key =input("Enter ID to update")
        found = False
        for e in lstemp:
            if str(e.eid)== key:
                print("\nEmployee Found")
                e.putdata()

                print("\nEnter New Employee Details")
                e.getData()
                e.calcsalary()

                print("Employee updated successfully")
                break

        if not found:
            print("Employee ID not found")
    elif ch==5:
        key =input("Enter ID to Delete")
        found = False
        for e in lstemp:
            if str(e.eid)== key:
                found = True
                lstemp.remove(e)
                print("Employee deleted successfully")
                break
        if not found:
            print("Employee Id not found")
    elif ch == 6:
        print("Exiting...")
        break
    else:
        print("Invalid choice")