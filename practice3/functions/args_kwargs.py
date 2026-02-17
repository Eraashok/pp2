def sum_all(*args: int) -> int:
    return sum(args)

def build_profile(**kwargs) -> dict:
    return kwargs

if __name__ == "__main__":
    print(sum_all(1, 2, 3, 4, 5))
    print(build_profile(name="Aibek", age=18, major="IS"))
