#1
import math

d = float(input())
r = d * math.pi / 180
print(round(r, 6))
#2
h = float(input())
a = float(input())
b = float(input())

s = (a + b) * h / 2
print(s)
#3
import math

n = int(input())
a = float(input())

s = (n * a * a) / (4 * math.tan(math.pi / n))
print(round(s, 2))
#4
a = float(input())
h = float(input())
s = a * h
print(float(s))