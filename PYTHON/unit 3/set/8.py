# Elements present in first set but not second
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7}

diff_a_b = set_a - set_b
diff_b_a = set_b - set_a

print("Set A - Set B:", diff_a_b)
print("Set B - Set A:", diff_b_a)