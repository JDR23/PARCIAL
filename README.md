# PARCIAL
Tienda online
# 🛒 Tienda Online en Python (Consola)
 
Este es el desarrollo del parcial # 1 de la clase Programacion del profe Alejandro Salgar en lenguaje Python que simula una tienda online con productos **Electrodomésticos**, **Ropa** y **Alimentos**, donde el usuario puede:
 
- Ver catálogo
- Agregar productos al carrito
- Remover productos del carrito
- Ver resumen del carrito
- Aplicar descuentos
- Calcular subtotal, descuentos y total a pagar
- Confirmar pago
 
Este programa está desarrollado siguiendo principios de **Programación Orientada a Objetos (POO)**:
- **Herencia**
- **Polimorfismo**
- **Encapsulamiento**
 
Además, el código está separado en diferentes archivos `.py` para mantener buenas prácticas de organización.
 
---
 
## 🚀 Instrucciones de instalación y ejecución
 
### 1. Clonar el repositorio
Abra una terminal (CMD, PowerShell o Git Bash) y ejecute:
 
```bash
 
git clone https://github.com/JDR23/PARCIAL-1.git
 
```
```bash
Ingresa al proyecto
    cd tienda-online-python
 
El programa se ejecuta desde el archivo main.py:
    python main.py
Esto abrirá un menú interactivo en la consola.
Estructura del proyecto
 
tienda-online-python/
│
├── product.py       # Clase base abstracta Product
├── appliance.py     # Subclase Appliance (Electrodomésticos)
├── clothing.py      # Subclase Clothing (Ropa)
├── food.py          # Subclase Food (Alimentos)
├── cart.py          # Carrito de compras (manejo de productos y descuentos)
├── discounts.py     # Estrategias de descuento (polimorfismo)
├── store.py         # Inventario inicial con productos
├── main.py          # Menú principal y flujo del programa
└── README.md        # Documentación del proyecto
```
 
### Explicación de clases y archivos
 
**Clase: product.py**
 
- Clase abstracta Product:
    Atributos encapsulados (id, name, price, stock).
 
- Métodos:
 
    * reserve() → Reserva stock si hay suficiente.
 
    * release() → Devuelve stock.
 
    * line_total() → Calcula el precio por cantidad.
   
    * Polimorfismo: cada subclase implementa category.
 
**Clase: appliance.py**
 
Clase Appliance (Electrodomésticos).
Atributos adicionales: warranty_months.
 
    * Ejemplo: Licuadora Pro 900W.
 
**clothing.py**
 
Clase Clothing (Ropa).
Atributos adicionales: size, gender.
 
    * Ejemplo: Jean Slim talla 32.
 
**Clase: food.py**
 
Clase Food (Alimentos).
Atributo adicional: expiration_date.
 
    * Ejemplo: Café Orgánico con fecha de vencimiento.
 
**discounts.py**
 
Define las estrategias de descuento usando polimorfismo:
 
- DiscountStrategy (abstracta).
- PercentageCoupon: Aplica un % al subtotal.
- CategoryDiscount: Aplica un % a productos de una categoría específica.
 
**Clase: cart.py**
 
Clase Cart que maneja el carrito:
 
Métodos principales:
 
- add_item() → Agregar producto.
- remove_item() → Remover producto.
- clear() → Vaciar carrito.
- add_discount() → Agregar descuentos.
- subtotal() → Calcula el subtotal.
- total_discount() → Calcula descuentos aplicados.
- total() → Subtotal - descuentos.
- summary() → Muestra un resumen detallado del carrito.
 
**Clase: store.py**
 
Función load_inventory() que carga un inventario inicial con productos de prueba.
 
**Clase: main.py**
 
Contiene el menú interactivo que se muestra al usuario:
 
```bash
 
1. Ver catálogo
2. Agregar al carrito
3. Remover del carrito
4. Ver carrito
5. Aplicar descuento
6. Limpiar descuentos
7. Pagar
8. Salir
```
 
**Ejemplo de uso en consola:**
 
```bash
==============================
    TIENDA ONLINE - CONSOLA
==============================
 
1) Ver catalogo
2) Agregar al carrito
3) Remover del carrito
4) Ver carrito
5) Aplicar descuento
6) Limpiar descuentos
7) Pagar
8) Salir
Seleccione opción:
 
```
 
### Ejemplo ejecucion
 
**1. Ver catálogo:**
 
* [1] Licuadora Pro 900W - $249,900.00 (Electrodomésticos) | Garantía: 24 meses
 
* [3] Camiseta Básica - $49,900.00 (Ropa) | Talla: M | Género: Unisex
 
* [5] Café Orgánico 500g - $34,900.00 (Alimentos) | Vence: 2026-02-28
 
 
 
**2. Agregar productos:**
 
* ID del producto a agregar: 3
 
* Cantidad: 2
 
* Agregado: Camiseta Básica x2
 
 
**3. Ver carrito:**
 
=== Carrito ===
 
Camiseta Básica x2 = $99,800.00 (Ropa)
 
Subtotal: $99,800.00
 
Total a pagar: $99,800.00
 
**4. Aplicar descuento:**
 
- Ingrese código: ROPA15
 
Descuento por categoría aplicado.
 
**5. Ver carrito con descuento:**
 
* Subtotal: $99,800.00
* Descuentos aplicados:
  - Descuento por categoría 'ropa' (-15%)
* Total descuento: -$14,970.00
* Total a pagar: $84,830.00
 
 
### Principios de POO aplicados
 
* Herencia: Appliance, Clothing y Food heredan de Product.
* Polimorfismo:
    * Cada producto implementa category.
    * Estrategias de descuento (PercentageCoupon, CategoryDiscount) calculan distinto.
* Encapsulamiento:
    * Atributos privados (_price, _stock) con getters/setters controlados.
    * Métodos (reserve, release) protegen la lógica del stock.
 
### Notas:
 
a. No se usaron try/except: validación manual de entradas.
 
b. El stock se actualiza automáticamente al agregar/remover productos.
 
c. El programa es interactivo por consola y se ejecuta solo con Python (no requiere librerías externas).
