# copy 1 file data to another

with open("2.txt","r") as f1:
    f2=open("destination.txt","w")
    f2.write(f1.read())
    f2.close()
with open("destination.txt","r") as f2:
    print(f1.read())