# maximum of 4 nos
a,b,c,d=int(input("Enter two Number :").split())
if a > b and a>c and a>d:
    print(a)
elif b>a and b>c and b>d:
    print(b)
elif c>a and c>b and c>d:
    print(c)
else:
    print(d)