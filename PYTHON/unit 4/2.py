# program to write dictionary

student={
    "name":"rahul",
    "age":18,
    "course":"mscit"
}
f1=open("name.txt","w")
for key,value in student.items():
    print(key,"=",value)