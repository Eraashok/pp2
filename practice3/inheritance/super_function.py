class A:
    def __init__(self):
        print("Parent")

class B(A):
    def __init__(self):
        super().__init__()
        print("Child")

b = B()
