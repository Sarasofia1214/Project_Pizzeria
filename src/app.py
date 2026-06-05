import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.cliente_service import ClienteService
from src.services.producto_service import ProductoService
from src.services.pedido_service import PedidoService
from src.config.database import dbInstance

def mainMenu():
    """Muestra el menú principal en español."""
    print("\n" + "="*50)
    print("🚲 CAMPUSBIKE - SISTEMA DE GESTIÓN")
    print("="*50)
    print("1. 👥 Clientes")
    print("2. 🚲 Productos")
    print("3. 📦 Pedidos")
    print("0. 🚪 Salir")

def customerMenu():
    """Submenú de gestión de clientes."""
    while True:
        print("\n--- CLIENTES ---")
        print("1. Crear cliente")
        print("2. Listar todos los clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("0. Volver")
        opt = input("Opción: ")

        if opt == '1':
            name = input("Nombre: ")
            address = input("Dirección: ")
            phone = input("Teléfono: ")
            balance = input("Saldo inicial (opcional): ")
            balance = float(balance) if balance else 0.0
            ClienteService.createCustomer(name, address, phone, balance)

        elif opt == '2':
            customers = ClienteService.getAllCustomers()
            if not customers:
                print("No hay clientes registrados.")
            else:
                print(f"{'ID':<5} {'Nombre':<20} {'Dirección':<20} {'Teléfono':<15} {'Saldo':<10}")
                print("-"*70)
                for c in customers:
                    print(f"{c[0]:<5} {c[1]:<20} {c[2] or '':<20} {c[3] or '':<15} ${c[4]:<10.2f}")

        elif opt == '3':
            customerId = int(input("ID del cliente: "))
            name = input("Nuevo nombre (vacío para omitir): ")
            address = input("Nueva dirección: ")
            phone = input("Nuevo teléfono: ")
            balance = input("Nuevo saldo: ")
            balance = float(balance) if balance else None
            ClienteService.updateCustomer(
                customerId,
                nombre=name if name else None,
                direccion=address if address else None,
                telefono=phone if phone else None,
                saldoActual=balance
            )
            print("Actualización intentada (si el ID existe).")
        elif opt == '4':
            customerId = int(input("ID del cliente a eliminar: "))
            if ClienteService.deleteCustomer(customerId):
                pass
            else:
                print("❌ No se pudo eliminar (quizás tiene pedidos asociados).")
        elif opt == '0':
            break

def productMenu():
    while True:
        print("\n--- PRODUCTOS ---")
        print("1. Listar productos")
        print("2. Actualizar precio de producto")
        print("3. Actualizar stock de producto")
        print("4. Registrar entrada de stock (compra)")  
        print("0. Volver")
        opt = input("Opción: ")

        if opt == '1':
            products = ProductoService.getAllProducts()
            if not products:
                print("No hay productos registrados.")
            else:
                print(f"{'ID':<5} {'Tipo':<25} {'Stock':<8} {'Precio':<10} {'Detalles'}")
                print("-"*70)
                for p in products:
                    print(f"{p[0]:<5} {p[1]:<25} {p[2]:<8} ${p[3]:<10.2f} {p[4] or ''}")
        elif opt == '2':
            try:
                pid = int(input("ID del producto: "))
                newPrice = float(input("Nuevo precio: "))
                if ProductoService.updateProductPrice(pid, newPrice):
                    pass
                else:
                    print("❌ Producto no encontrado.")
            except ValueError:
                print("❌ Error: Debe ingresar un número válido para ID y precio.")
        elif opt == '3':
            try:
                pid = int(input("ID del producto: "))
                newStock = int(input("Nueva cantidad en stock: "))
                if ProductoService.updateProductStock(pid, newStock):
                    print("✅ Stock actualizado.")
                else:
                    print("❌ Producto no encontrado.")
            except ValueError:
                print("❌ Error: Debe ingresar un número entero para ID y cantidad de stock.")
        elif opt == '4':
            try:
                pid = int(input("ID del producto: "))
                cantidad = int(input("Cantidad que llega: "))
                precioCompra = float(input("Precio de compra unitario: "))
                proveedorId = int(input("ID del proveedor: "))
                ProductoService.addStock(pid, cantidad, precioCompra, proveedorId)
            except ValueError:
                print("❌ Error: debe ingresar números válidos.")
        elif opt == '0':
            break

def orderMenu():
    """Submenú de gestión de pedidos (incluye transacción)."""
    while True:
        print("\n--- PEDIDOS ---")
        print("1. Crear nuevo pedido")
        print("2. Listar todos los pedidos")
        print("3. Ver detalles de un pedido")
        print("0. Volver")
        opt = input("Opción: ")

        if opt == '1':
            # Mostrar clientes
            customers = ClienteService.getAllCustomers()
            if not customers:
                print("❌ No hay clientes. Por favor cree un cliente primero.")
                continue
            print("Clientes disponibles:")
            for c in customers:
                print(f"ID:{c[0]} - {c[1]}")
            custId = int(input("ID del cliente: "))

            # Mostrar productos
            products = ProductoService.getAllProducts()
            if not products:
                print("❌ No hay productos disponibles.")
                continue
            print("\nProductos disponibles:")
            for p in products:
                print(f"ID:{p[0]} | {p[1]} | Stock:{p[2]} | Precio:${p[3]}")
            prodId = int(input("ID del producto: "))
            quantity = int(input("Cantidad: "))
            color = input("Color (opcional): ") or None
            size = input("Tamaño (opcional): ") or None
            customName = input("Nombre del pedido (opcional): ") or None

            result = PedidoService.createOrder(custId, prodId, quantity, color, size, customName)
            if result:
                print(f"✅ Pedido #{result['orderId']} creado. Total: ${result['total']:.2f}")
            else:
                print("❌ No se pudo completar el pedido.")

        elif opt == '2':
            orders = PedidoService.getAllOrders()
            if not orders:
                print("No hay pedidos registrados.")
            else:
                print(f"{'ID':<6} {'Cliente':<20} {'Nombre Pedido':<20} {'Total':<10} {'Fecha'}")
                print("-"*70)
                for o in orders:
                    print(f"{o[0]:<6} {o[1] or 'N/A':<20} {o[2] or '':<20} ${o[3]:<10.2f} {o[4]}")
        elif opt == '3':
            oid = int(input("ID del pedido: "))
            details = PedidoService.getOrderDetails(oid)
            if details:
                print(f"\nPedido #{details['id']}")
                print(f"Cliente: {details['cliente']}")
                print(f"Nombre: {details['nombre']}")
                print(f"Descripción: {details['descripcion']}")
                print(f"Color: {details['color']}, Tamaño: {details['tamano']}")
                print(f"Total: ${details['precio']:.2f}")
                print(f"Fecha: {details['fecha']}")
            else:
                print("Pedido no encontrado.")
        elif opt == '0':
            break

def main():
    """Función principal: prueba conexión y lanza el menú."""
    # Probar conexión a la base de datos
    try:
        conn = dbInstance.connect()
        dbInstance.disconnect(conn)
        print("✅ Conectado a la base de datos CampusBike")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    while True:
        mainMenu()
        choice = input("Seleccione: ")
        if choice == '1':
            customerMenu()
        elif choice == '2':
            productMenu()
        elif choice == '3':
            orderMenu()
        elif choice == '0':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()