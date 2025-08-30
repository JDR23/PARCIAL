from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final


class Product(ABC):
    """
    Clase base (abstracta) para productos.
    Encapsula atributos y expone propiedades controladas.
    """

    def __init__(self, pid: int, name: str, price: float, stock: int) -> None:
        self._id: Final[int] = pid
        self._name: str = name
        self._price: float = price
        self._stock: int = stock

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value >= 0:
            self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value >= 0:
            self._stock = value

    @property
    @abstractmethod
    def category(self) -> str:
        """Cada subclase define su categoría."""
        ...

    def reserve(self, qty: int) -> bool:
        """Reserva (disminuye) stock si hay disponibilidad."""
        if qty <= 0:
            return False
        if qty <= self._stock:
            self._stock -= qty
            return True
        return False

    def release(self, qty: int) -> None:
        """Libera (aumenta) stock, usado al remover del carrito."""
        if qty > 0:
            self._stock += qty

    def line_total(self, qty: int) -> float:
        return self._price * max(qty, 0)

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} - ${self.price:,.2f} ({self.category}) | Stock: {self.stock}"
