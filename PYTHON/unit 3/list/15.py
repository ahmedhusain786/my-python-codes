L1 = ["Amit", "Rahul", "Neha"]

print(len(L1))          # Returns total number of elements.
print(max([10,20,5]))   # Returns the largest element.
print(min([10,20,5]))   # Returns the smallest element.
print(sum([1,2,3]))     # Returns the total of all numbers.
print(sorted(L1))       # Returns a new sorted list.
L1.sort()               # Sorts the original list.
L1.reverse()            # Reverses the list.
L1.append("Riya")       # Adds one element at the end.
L1.extend(["A","B"])    # Adds multiple elements.
L1.insert(1,"Karan")    # Inserts element at given index.
L1.remove("Rahul")      # Removes first matching element.
L1.pop()                # Removes and returns last element.
L1.pop(1)               # Removes element at given index.
L1.clear()              # Removes all elements.
print(L1.count("Amit")) # Counts occurrences of an element.
print(L1.index("Amit")) # Returns first index of element.
print("Amit" in L1)     # Checks if element exists.
print("Raj" not in L1)  # Checks if element does not exist.
L2 = L1.copy()          # Creates a copy of the list.