t = (45,12,78,34,99,10,67)

maximum = t[0]
minimum = t[0]

for i in t:

    if i > maximum:
        maximum = i

    if i < minimum:
        minimum = i

print("Maximum =", maximum)
print("Minimum =", minimum)