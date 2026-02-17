class A:
    def say(self):
        print("A")

class B:
    def hello(self):
        print("B")

class C(A, B):
    pass

c = C()
c.say()
c.hello()
