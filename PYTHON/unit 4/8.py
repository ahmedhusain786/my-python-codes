# counting number  of uppercase and lowercase
# count number of vowels
f1=open("2.txt","r")
data= f1.read()
ucount = 0
lcount = 0
for i in data:
    if i.isupper():
        ucount = ucount + 1
    elif i.islower():
        lcount= lcount + 1
print("Total number of Upper case :",ucount)
print("Total number of lower case :",lcount)