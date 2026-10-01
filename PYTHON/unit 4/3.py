# store 5 students name in python
f1=open("2.txt","w")
for i in range(1,6):
    nm= input("Enter the name")
    f1.write(nm)
    f1.write("\n")
f1.close()
f1=open("2.txt","r")
nm= f1.read()
print("Name is :",nm)