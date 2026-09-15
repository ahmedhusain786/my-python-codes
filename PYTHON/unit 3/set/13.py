# Modifying sets directly in place
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}

s1.intersection_update(s2)  # s1 now contains only elements common to both
print("s1 after intersection_update:", s1)