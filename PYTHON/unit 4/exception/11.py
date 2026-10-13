# Exception

try:
    a=5
    b=2
    c=0
    d=int("abc")
    e= a/c
except ZeroDivisionError:
    print("cannot be div by zero")
except ValueError as e:
    print(e)
    print("Value error")
else:
    print("Execute when there is no error")
finally:
    print("always execute ")

