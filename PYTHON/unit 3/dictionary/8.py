# Looping through keys, values, and key-value pairs
scores = {"Math": 90, "Science": 85, "English": 88}

print("Keys:")
for k in scores.keys():
    print(k, end=" ")

print("\nValues:")
for v in scores.values():
    print(v, end=" ")

print("\nItems:")
for k, v in scores.items():
    print(k,v)