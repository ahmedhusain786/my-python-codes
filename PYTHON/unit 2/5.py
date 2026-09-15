# pass by reference

def change(number):
    number.append(100)
l1=[10,20,30]
change(l1)
print(l1)
