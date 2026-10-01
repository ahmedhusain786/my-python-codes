# count number of vowels
f1=open("2.txt","r")
data= f1.read()
count = 0
for i in data:
    if i in "aeiouAeiou":
        count = count + 1
print("Total number of vowels are:",count)