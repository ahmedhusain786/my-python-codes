# Removing elements safely and unsafely
numbers = {10, 20, 30, 40, 50}

numbers.remove(20)       # Raises KeyError if not found
numbers.discard(99)      # Safe: Does nothing if element doesn't exist
popped = numbers.pop()   # Removes and returns an arbitrary element

print("Popped Element:", popped)
print("Remaining Set:", numbers)