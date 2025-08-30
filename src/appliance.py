from typing import Final
from product import Product


class Appliance(Product):
    """Electrodomésticos"""

    def __init__(self, pid: int, name: str, price: float, stock: int, warranty_months: int) -> None:
        super().__init__(pid, name, price, stock)
        self._warranty_months: Final[int] = warranty_months

    @property
    def warranty_months(self) -> int:
        return self._warranty_months

    @property
    def category(self) -> str:
        return "Electrodomésticos"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Garantía: {self.warranty_months} meses"
