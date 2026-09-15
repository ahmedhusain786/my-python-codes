import crud as c1
while True:
    print("=====================================================")
    print("             LIBRARY MANAGEMENT SYSTEM               ")
    print("=====================================================")
    print("1.Add Book\n2.View Books\n3.Search Book\n4.Update Book\n5.Delete Book\n6.Sort Books\n7.Exit")
    choice=int(input("Enter your choice (1-7) :"))
    if choice==1:
        c1.addbook()
    elif choice==2:
        c1.viewbook()
    elif choice==3:
        c1.searchbook()
    elif choice==4:
        c1.updatebook()
    elif choice==5:
        c1.deletebook()
    elif choice==6:
        c1.sortbook()
    elif choice==7:
        print("Exiting...")
        break
    else:
        print("Invalid Choice")
