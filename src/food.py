from datetime import date
from product import Product


class Food(Product):
    """Alimentos"""

    def __init__(self, pid: int, name: str, price: float, stock: int, expiration_date: date) -> None:
        super().__init__(pid, name, price, stock)
        self._expiration_date: date = expiration_date

    @property
    def expiration_date(self) -> date:
        return self._expiration_date

    @property
    def category(self) -> str:
        return "Alimentos"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Vence: {self.expiration_date.isoformat()}"