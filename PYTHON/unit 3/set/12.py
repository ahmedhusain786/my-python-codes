# Cleaning duplicate values using list -> set conversion
duplicates_list = [10, 20, 10, 30, 20, 40, 50, 40]

unique_set = set(duplicates_list)
cleaned_list = list(unique_set)

print("Original List:", duplicates_list)
print("Cleaned List :", cleaned_list)