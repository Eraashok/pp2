def min_max(numbers: list[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)

def is_even(n: int) -> bool:
    return n % 2 == 0

if __name__ == "__main__":
    data = [10, 3, 25, 7, 14]
    print(min_max(data))
    print(is_even(14))
    print(is_even(7))
