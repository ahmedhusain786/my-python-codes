# Accessing keys using bracket notation and .get() with defaults
student = {"name": "Aniket", "age": 21, "course": "M.Sc. IT"}

print("Name:", student["name"])
print("Age:", student.get("age"))
print("Grade (Default):", student.get("grade", "Not Assigned"))