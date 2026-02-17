students = [
    {"name": "Ali", "gpa": 3.2},
    {"name": "Dana", "gpa": 3.8},
    {"name": "Mira", "gpa": 3.5},
]

sorted_by_gpa = sorted(students, key=lambda s: s["gpa"])
sorted_by_name_desc = sorted(students, key=lambda s: s["name"], reverse=True)

if __name__ == "__main__":
    print(sorted_by_gpa)
    print(sorted_by_name_desc)
