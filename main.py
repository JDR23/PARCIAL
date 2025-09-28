from database import Base, engine, SessionLocal
from models import Usuario
from datetime import datetime

# Crear las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)


def crear_usuario(db):
    print("\n--- Crear Usuario ---")
    primer_nombre = input("Primer nombre: ")
    segundo_nombre = input("Segundo nombre (opcional): ")
    primer_apellido = input("Primer apellido: ")
    segundo_apellido = input("Segundo apellido (opcional): ")
    rol = input("Rol: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

    usuario = Usuario(
        primer_nombre_usuario=primer_nombre,
        segundo_nombre_usuario=segundo_nombre or None,
        primer_apellido_usuario=primer_apellido,
        segundo_apellido_usuario=segundo_apellido or None,
        rol_usuario=rol,
        fecha_nacimiento_usuario=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    print(f"✅ Usuario creado con ID: {usuario.id}")


def listar_usuarios(db):
    print("\n--- Lista de Usuarios ---")
    usuarios = db.query(Usuario).all()
    if not usuarios:
        print("No hay usuarios registrados.")
    for u in usuarios:
        print(
            f"{u.id} | {u.primer_nombre_usuario} {u.primer_apellido_usuario} - {u.rol_usuario}"
        )


def actualizar_usuario(db):
    listar_usuarios(db)
    usuario_id = input("\nIngrese el ID del usuario a actualizar: ")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        print("❌ Usuario no encontrado")
        return

    nuevo_nombre = (
        input(f"Nuevo primer nombre ({usuario.primer_nombre_usuario}): ")
        or usuario.primer_nombre_usuario
    )
    nuevo_apellido = (
        input(f"Nuevo primer apellido ({usuario.primer_apellido_usuario}): ")
        or usuario.primer_apellido_usuario
    )
    nuevo_rol = input(f"Nuevo rol ({usuario.rol_usuario}): ") or usuario.rol_usuario

    usuario.primer_nombre_usuario = nuevo_nombre
    usuario.primer_apellido_usuario = nuevo_apellido
    usuario.rol_usuario = nuevo_rol

    db.commit()
    print("✅ Usuario actualizado con éxito")


def eliminar_usuario(db):
    listar_usuarios(db)
    usuario_id = input("\nIngrese el ID del usuario a eliminar: ")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        print("❌ Usuario no encontrado")
        return

    db.delete(usuario)
    db.commit()
    print("✅ Usuario eliminado con éxito")


def menu():
    db = SessionLocal()
    while True:
        print("\n=== MENÚ GESTIÓN DE USUARIOS ===")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            crear_usuario(db)
        elif opcion == "2":
            listar_usuarios(db)
        elif opcion == "3":
            actualizar_usuario(db)
        elif opcion == "4":
            eliminar_usuario(db)
        elif opcion == "5":
            db.close()
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    menu()
