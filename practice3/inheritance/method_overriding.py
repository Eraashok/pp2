class A:
    def say(self):
        print("A")

class B(A):
    def say(self):
        print("B")

b = B()
b.say()
