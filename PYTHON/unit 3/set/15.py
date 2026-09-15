# Shallow copying and clearing set content
original = {10, 20, 30}
copied_set = original.copy()

original.clear()

print("Original Set after clear():", original)
print("Copied Set:", copied_set)