# prime number
n=int(input("Enter the N:"))
cnt=0
for i in range(n,n+1):
        if n%i==0:
            cnt+=1
        if cnt>2:
            break
print(cnt)
if cnt==2:
       print(n,"is prime no")
else:
       print(n,"is not prime no")