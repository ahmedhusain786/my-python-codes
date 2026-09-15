# Pairing two lists into a dictionary using zip()
keys = ["name", "age", "city"]
values = ["Priya", 22, "Surat"]

profile = dict(zip(keys, values))
print("Zipped Dictionary:", profile)