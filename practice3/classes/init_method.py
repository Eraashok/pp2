class Student:
    def __init__(self, name: str, major: str) -> None:
        self.name = name
        self.major = major

    def info(self) -> None:
        print(self.name, self.major)

if __name__ == "__main__":
    s = Student("Aibek", "Information Systems")
    s.info()
