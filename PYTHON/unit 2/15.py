# filtering odd numbers
numbers = [10, 15, 20, 25, 30, 35, 40]

result = list(filter(lambda x: x % 2 != 0, numbers))

print(result)