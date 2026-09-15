# fibonaaci number using while
n=int(input("Enter N"))
a,b=1,1
print(a,end=" ")
print(b,end=" ")
while(1):
    c=a+b
    a=b
    b=c

    if c>n:
        break
    else:
        print(c,end=" ")
    print(end=" ")
    