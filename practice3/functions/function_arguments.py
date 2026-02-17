def introduce(name: str, city: str = "Almaty") -> None:
    print(f"{name} from {city}")

def power(base: int, exp: int = 2) -> int:
    return base ** exp

if __name__ == "__main__":
    introduce("Dana")
    introduce("Dana", "Astana")
    print(power(3))
    print(power(3, 4))
