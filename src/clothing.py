from product import Product


class Clothing(Product):
    """Ropa"""

    def __init__(self, pid: int, name: str, price: float, stock: int, size: str, gender: str) -> None:
        super().__init__(pid, name, price, stock)
        self._size: str = size
        self._gender: str = gender

    @property
    def size(self) -> str:
        return self._size

    @property
    def gender(self) -> str:
        return self._gender

    @property
    def category(self) -> str:
        return "Ropa"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Talla: {self.size} | Género: {self.gender}"