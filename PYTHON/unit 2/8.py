# global keyword
count=10
def change():
    global count
    count=20
change()
print(count)