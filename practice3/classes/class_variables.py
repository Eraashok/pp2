class Laptop:
    brand = "DefaultBrand"

    def __init__(self, model: str) -> None:
        self.model = model

if __name__ == "__main__":
    l1 = Laptop("Model-A")
    l2 = Laptop("Model-B")

    print(Laptop.brand)
    print(l1.brand, l1.model)
    print(l2.brand, l2.model)

    l1.brand = "ASUS"
    print(Laptop.brand)
    print(l1.brand)
    print(l2.brand)
