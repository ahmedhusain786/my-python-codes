L1 = ["Amit", "Rahul", "Neha"]

name = input("Enter student name: ")

if name in L1:
    L1.remove(name)
    print(L1)
else:
    print("Student Not Found")