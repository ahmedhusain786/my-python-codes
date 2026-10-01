# count character , word
f1=open("2.txt","r")
nm= f1.read()
print("Total character are:",len(nm))
wrd= nm.split()
print("Total words are :",len(wrd))