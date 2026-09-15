vowels = ('a','e','i','o','u','A','E','I','O','U')

s = input("Enter String: ")

count = 0

for ch in s:

    if ch in vowels:
        count += 1

print("Vowels =", count)