# armstrong number

n=int(input("Enter the N:"))
rev=0
rem=None
temp=n
while(n!=0):
    rem=n%10
    rev=(rev*10) + rem*rem*rem
    n=n//10
if temp==rev:
    print(rev,"Is armstrong number")
else:
    print(rev,"Is not armstrong number")