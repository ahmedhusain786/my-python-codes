# program to write and read data in a file

f1=open("1.txt","w")
f1.write("hello")
f1.close()
f1=open("1.txt","r")
nm= f1.read()
print(nm)