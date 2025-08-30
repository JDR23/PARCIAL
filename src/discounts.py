from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Iterable, Tuple
from product import Product


class DiscountStrategy(ABC):
    """
    Estrategia de descuento (Patrón Estrategia).
    Polimorfismo: cada implementación calcula el descuento de forma distinta.
    """

    @abstractmethod
    def compute(self, items: Dict[int, Tuple[Product, int]], subtotal: float) -> float:
        """Retorna el monto de descuento (>= 0)."""
        ...


class PercentageCoupon(DiscountStrategy):
    def __init__(self, code: str, percent: float) -> None:
        self._code = code.upper().strip()
        self._percent = percent

    @property
    def code(self) -> str:
        return self._code

    def compute(self, items: Dict[int, Tuple[Product, int]], subtotal: float) -> float:
        if self._percent <= 0 or subtotal <= 0:
            return 0.0
        return subtotal * (self._percent / 100.0)

    def __str__(self) -> str:
        return f"Cupón {self.code} (-{self._percent:.0f}%)"


class CategoryDiscount(DiscountStrategy):
    def __init__(self, category: str, percent: float) -> None:
        self._category = category.strip().lower()
        self._percent = percent

    @property
    def category(self) -> str:
        return self._category

    def compute(self, items: Dict[int, Tuple[Product, int]], subtotal: float) -> float:
        if self._percent <= 0:
            return 0.0
        eligible_total = 0.0
        for _, (product, qty) in items.items():
            if product.category.lower() == self._category and qty > 0:
                eligible_total += product.line_total(qty)
        return eligible_total * (self._percent / 100.0)

    def __str__(self) -> str:
        return f"Descuento por categoría '{self.category}' (-{self._percent:.0f}%)"
