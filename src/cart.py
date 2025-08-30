from __future__ import annotations
from typing import Dict, Tuple, List
from .product import Product
from .discounts import DiscountStrategy


class Cart:
    """
    Carrito con encapsulamiento de items y estrategias de descuento.
    """

    def __init__(self) -> None:
        self._items: Dict[int, Tuple[Product, int]] = {}
        self._discounts: List[DiscountStrategy] = []

    @property
    def items(self) -> Dict[int, Tuple[Product, int]]:
        return self._items

    @property
    def discounts(self) -> List[DiscountStrategy]:
        return self._discounts

    def add_item(self, product: Product, qty: int) -> bool:
        if qty <= 0:
            return False
        if not product.reserve(qty):
            return False
        if product.id in self._items:
            current_qty = self._items[product.id][1]
            self._items[product.id] = (product, current_qty + qty)
        else:
            self._items[product.id] = (product, qty)
        return True

    def remove_item(self, product_id: int, qty: int) -> bool:
        if product_id not in self._items or qty <= 0:
            return False
        product, current_qty = self._items[product_id]
        if qty >= current_qty:
            # liberar todo
            product.release(current_qty)
            del self._items[product_id]
        else:
            product.release(qty)
            self._items[product_id] = (product, current_qty - qty)
        return True

    def clear(self) -> None:
        # devolver stock
        for _, (p, q) in self._items.items():
            p.release(q)
        self._items = {}
        self._discounts = []

    def add_discount(self, strategy: DiscountStrategy) -> None:
        self._discounts.append(strategy)

    def clear_discounts(self) -> None:
        self._discounts = []

    def subtotal(self) -> float:
        total = 0.0
        for _, (p, q) in self._items.items():
            total += p.line_total(q)
        return total

    def total_discount(self) -> float:
        sub = self.subtotal()
        total_disc = 0.0
        for strat in self._discounts:
            total_disc += max(0.0, strat.compute(self._items, sub))
        # Evitar descuento mayor al subtotal
        if total_disc > sub:
            total_disc = sub
        return total_disc

    def total(self) -> float:
        return self.subtotal() - self.total_discount()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def summary(self) -> str:
        lines: List[str] = []
        lines.append("=== Carrito ===")
        if self.is_empty():
            lines.append("Vacío.")
        else:
            for _, (p, q) in self._items.items():
                lines.append(f"- {p.name} x{q} = ${p.line_total(q):,.2f} ({p.category})")
            lines.append(f"Subtotal: ${self.subtotal():,.2f}")
            if len(self._discounts) > 0:
                lines.append("Descuentos aplicados:")
                for d in self._discounts:
                    lines.append(f"  • {d}")
                lines.append(f"Total descuento: -${self.total_discount():,.2f}")
            lines.append(f"Total a pagar: ${self.total():,.2f}")
        return "\n".join(lines)