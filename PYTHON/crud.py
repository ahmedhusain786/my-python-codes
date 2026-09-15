library=[]
def addbook():
    global library
    id=int(input("Enter Book ID:"))
    title=input("Enter Book Title:")
    author=input("Enter Author:")
    category=input("Enter Category:")
    price=float(input("Enter Price :"))

    l1={
        "BID":id,
        "Btitle":title,
        "Bauthor":author,
        "Bcat":category,
        "Bprice":price
    }
    library.append(l1)
    print("Book Added Successfully !")

def viewbook():
    print("==================================================================================")
    print("BOOK ID   |   BOOK TITLE   |   BOOK AUTHOR    |   BOOK CATEGORY    |    BOOK PRICE")
    print("==================================================================================")
    for l1 in library:
        print(l1["BID"],"             ",l1["Btitle"],"         ",l1["Bauthor"],"        ",l1["Bcat"],"      ",l1["Bprice"])
    print("==================================================================================")
def searchbook():
    id=int(input("Enter ID To Search :"))
    found=0
    for l1 in library:
        if l1["BID"]==id:
            found=1
            break
    if found==1:
        print(" Book Found Successfully !")
        viewbook()
    else:
        print("Book Not found")
def updatebook():
    id=int(input("Enter ID To Update :"))
    found=0
    for l1 in library:
        if l1["BID"]==id:
            found=1
            break
    if found==1:
        n_title=input("Enter New Title:")
        n_author=input("Enter New Author Name:")
        n_cat=input("Enter New Category:")
        n_price=float(input("Enter New Price:"))
        l1["Btitle"]=n_title
        l1["Bauthor"]=n_author
        l1["Bcat"]=n_cat
        l1["Bprice"]=n_price
        viewbook()
    else:
        print("Book Not found")

def deletebook():
    id=int(input("Enter ID To Delete :"))
    found=0
    for l1 in library:
        if l1["BID"]==id:
            found=1
            break
    if found==1:
        library.remove(l1)
        print("Book Deleted Successfully")
        viewbook()
    else:
        print("Book Not found")
def sortbook():
    if not library:
        print("Book is not available to sort")
        return
    print("\n1.Sort By Book ID")
    print("2. Sort By Book Title") 
    print("3. Sort By Author") 
    print("4. Sort By Price") 
    choice = int(input("Enter Your Choice: ")) 
    if choice == 1:
        library.sort(key= lambda x : x["BID"])
        print("Book Sorted By ID")
    elif choice ==2:
        library.sort(key= lambda x : x["Btitle"])
        print("Book Sorted By Book Title")
    elif choice==3:
        library.sort(key=lambda x : x["Bauthor"])
        print("Book Sorted By Author Name")
    elif choice==4:
        library.sort(key=lambda x : x["Bprice"])
        print("Book Sorted By Price")
    else:
        print("invalid choice")
    viewbook()

    




    