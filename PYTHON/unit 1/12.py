# palindrome no

n=int(input("Enter the N:"))
rev=0
rem=None
temp=n
while(n!=0):
    rem=n%10
    rev=(rev*10) + rem
    n=n//10
if temp==rev:
    print(rev,"Is palindrome number")
else:
    print(rev,"Is not palindrome number")