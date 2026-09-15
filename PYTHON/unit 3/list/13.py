L = [10,15,8,5,9,20,7,18,11,4]

odd = 0
even = 0

for i in L:
    if i % 2 == 0:
        even += i
    else:
        odd += i

print("Even Total =", even)
print("Odd Total =", odd)