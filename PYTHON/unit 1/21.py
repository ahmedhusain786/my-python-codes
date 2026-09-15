# pattern
k=5
for i in range(1,6):
    for j in range(1,k):
        print(" ",end="")
        k-=1
        for j in range(1,i+1):
            print(k,end=" ")
        print()