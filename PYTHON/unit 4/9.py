# count char,alpha,whitespace,symbol
# count number of vowels
f1=open("2.txt","r")
data= f1.read()
chrcount =0
wcount=0
digcount=0
symcnt=0
for i in data:
    if i.isupper() or i.islower():
        chrcount = chrcount + 1
    elif i.isdigit():
        digcount=digcount+1
    elif i.isspace():
        wcount=wcount+1
    else:
        symcnt=symcnt+1
print(chrcount,wcount,digcount,symcnt)