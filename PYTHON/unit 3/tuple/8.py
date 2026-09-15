t = (10,15,20,25,30,35,40,45,50,55)

odd = ()
even = ()

odd_list = []
even_list = []

for i in t:

    if i % 2 == 0:
        even_list.append(i)
    else:
        odd_list.append(i)

odd = tuple(odd_list)
even = tuple(even_list)

print("Odd =", odd)
print("Even =", even)