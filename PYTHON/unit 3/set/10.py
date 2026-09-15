# Checking subset/superset relationships
a = {1, 2}
b = {1, 2, 3, 4}

print("Is A subset of B?", a.issubset(b))
print("Is B superset of A?", b.issuperset(a))
print("Are A and B disjoint?", a.isdisjoint({5, 6}))