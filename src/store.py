from datetime import date, timedelta
from typing import Dict
from src.appliance import Appliance
from clothing import Clothing
from food import Food
from product import Product


def load_inventory() -> Dict[int, Product]:
    """
    Crea un inventario base con productos de:
    - Electrodomésticos
    - Ropa
    - Alimentos
    """
    today = date.today()
    inventory: Dict[int, Product] = {
        1: Appliance(1, "Licuadora Pro 900W", 249900.0, 10, warranty_months=24),
        2: Appliance(2, "Aspiradora Ciclónica", 399900.0, 5, warranty_months=18),
        3: Clothing(3, "Camiseta Básica", 49900.0, 30, size="M", gender="Unisex"),
        4: Clothing(4, "Jean Slim", 139900.0, 20, size="32", gender="Hombre"),
        5: Food(5, "Café Orgánico 500g", 34900.0, 40, expiration_date=today + timedelta(days=180)),
        6: Food(6, "Pasta Integral 1kg", 19900.0, 50, expiration_date=today + timedelta(days=365)),
    }
    return inventory
