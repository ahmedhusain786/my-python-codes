# Removing items using different deletion methods
data = {"a": 1, "b": 2, "c": 3, "d": 4}

removed_val = data.pop("b")  # Removes key 'b' and returns its value
last_item = data.popitem()  # Removes the last inserted key-value pair
del data["a"]               # Deletes key 'a'

print("Removed Val:", removed_val)
print("Last Item Removed:", last_item)
print("Remaining Dict:", data)