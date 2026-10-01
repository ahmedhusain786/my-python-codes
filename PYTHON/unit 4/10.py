# count number of vowels
f1=open("2.txt","r")
data= f1.read()
word = input("Enter word to search")
for i in data:
    if i in word:
        found = 1
        break
print("Found :",word)