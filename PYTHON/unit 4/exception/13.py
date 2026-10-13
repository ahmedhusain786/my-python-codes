class priceerror(Exception):
    pass
try:
    price= int(input("enter price:"))
    if price<0:
        raise priceerror("Price is negative")
except priceerror as e:
    print(e)