class Markserror(Exception):
    pass
try:
    marks= int(input("enter price:"))
    if marks >=0 and marks<=50:
        raise Markserror("Marks is between (0-50)")
except Markserror as e:
    print(e)
else:
    print("Marks is not between (0-50)")