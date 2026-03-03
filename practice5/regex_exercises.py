import re
# 1
print(bool(re.match(r"^ab*$", "abbb")))

# 2
print(bool(re.match(r"^ab{2,3}$", "abbb")))

# 3
print(bool(re.match(r"^[a-z]+_[a-z]+$", "hello_world")))

# 4
print(bool(re.match(r"^[A-Z][a-z]+$", "Hello")))

# 5
print(bool(re.match(r"^a.*b$", "axxxb")))

# 6
print(re.sub(r"[ ,\.]", ":", "Hello, world. Python"))

# 7
print(re.sub(r"_([a-z])", lambda m: m.group(1).upper(), "my_snake_case"))

# 8
print([x for x in re.split(r"(?=[A-Z])", "SplitAtUpperCase") if x])

# 9
print(re.sub(r"(?<!^)(?=[A-Z])", " ", "HelloWorldFromPython"))

# 10
print(re.sub(r"(?<!^)([A-Z])", r"_\1", "camelCaseString").lower())