L = ['a','b','e','f','i','o','u','k']

count = 0

for i in L:
    if i in "aeiouAEIOU":
        count += 1

print("Vowels =", count)