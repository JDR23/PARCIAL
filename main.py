from typing import Dict, Optional
from src.product import Product
from src.store import load_inventory
from src.cart import Cart
from src.discounts import PercentageCoupon, CategoryDiscount


def print_header() -> None:
    print("\n==============================")
    print("   TIENDA ONLINE - CONSOLA")
    print("==============================\n")


def print_menu() -> None:
    print("1) Ver catálogo")
    print("2) Agregar al carrito")
    print("3) Remover del carrito")
    print("4) Ver carrito")
    print("5) Aplicar descuento")
    print("6) Limpiar descuentos")
    print("7) Pagar")
    print("8) Salir")


def show_catalog(inventory: Dict[int, Product]) -> None:
    print("\n=== Catálogo ===")
    for pid, prod in inventory.items():
        print(prod)
    print("")


def input_int(prompt: str) -> Optional[int]:
    value = input(prompt).strip()
    if value.isdigit():
        return int(value)
    return None


def input_float(prompt: str) -> Optional[float]:
    value = input(prompt).strip().replace(",", ".")
    # validar formato simple (sin try/except)
    digits = "0123456789."
    if all((ch in digits) for ch in value) and value.count(".") <= 1 and value != "":
        if value.startswith(".") or value.endswith("."):
            return None
        return float(value)
    return None


def handle_add_to_cart(inventory: Dict[int, Product], cart: Cart) -> None:
    pid = input_int("ID del producto a agregar: ")
    if pid is None or pid not in inventory:
        print("ID inválido.")
        return
    qty = input_int("Cantidad: ")
    if qty is None or qty <= 0:
        print("Cantidad inválida.")
        return
    product = inventory[pid]
    ok = cart.add_item(product, qty)
    if ok:
        print(f"Agregado: {product.name} x{qty}")
    else:
        print("No hay stock suficiente o cantidad inválida.")


def handle_remove_from_cart(cart: Cart) -> None:
    pid = input_int("ID del producto a remover: ")
    if pid is None:
        print("ID inválido.")
        return
    qty = input_int("Cantidad a remover: ")
    if qty is None or qty <= 0:
        print("Cantidad inválida.")
        return
    ok = cart.remove_item(pid, qty)
    if ok:
        print("Removido del carrito.")
    else:
        print("No se pudo remover (verifique ID/cantidad).")


def handle_apply_discount(cart: Cart) -> None:
    print("\nCódigos disponibles (ejemplos):")
    print(" - COUPON10  => 10% al total")
    print(" - ELECTRO5  => 5% en Electrodomésticos")
    print(" - ROPA15    => 15% en Ropa")
    print(" - ALI20     => 20% en Alimentos\n")
    code = input("Ingrese código: ").strip().upper()

    if code == "COUPON10":
        cart.add_discount(PercentageCoupon(code, 10.0))
        print("Cupón aplicado.")
    elif code == "ELECTRO5":
        cart.add_discount(CategoryDiscount("Electrodomésticos", 5.0))
        print("Descuento por categoría aplicado.")
    elif code == "ROPA15":
        cart.add_discount(CategoryDiscount("Ropa", 15.0))
        print("Descuento por categoría aplicado.")
    elif code == "ALI20":
        cart.add_discount(CategoryDiscount("Alimentos", 20.0))
        print("Descuento por categoría aplicado.")
    else:
        print("Código no reconocido.")


def handle_checkout(cart: Cart) -> None:
    print("\n" + cart.summary())
    if cart.is_empty():
        return
    confirm = input("¿Confirmar pago? (s/n): ").strip().lower()
    if confirm == "s":
        print(" Pago realizado. ¡Gracias por su compra!")
        cart.clear()
    else:
        print("Operación cancelada.")


def main() -> None:
    inventory = load_inventory()
    cart = Cart()

    while True:
        print_header()
        print_menu()
        choice = input("Seleccione opción: ").strip()

        if choice == "1":
            show_catalog(inventory)
        elif choice == "2":
            show_catalog(inventory)
            handle_add_to_cart(inventory, cart)
        elif choice == "3":
            handle_remove_from_cart(cart)
        elif choice == "4":
            print("\n" + cart.summary() + "\n")
        elif choice == "5":
            handle_apply_discount(cart)
        elif choice == "6":
            cart.clear_discounts()
            print("Descuentos eliminados.")
        elif choice == "7":
            handle_checkout(cart)
        elif choice == "8":
            print("Saliendo... ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

        input("\nPresione ENTER para continuar...")


if __name__ == "__main__":
    main()
