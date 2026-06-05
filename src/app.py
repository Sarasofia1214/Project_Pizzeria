#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.cliente_service import ClienteService
from src.services.producto_service import ProductoService
from src.services.pedido_service import PedidoService
from src.config.database import db_instance

def menu_principal():
    print("\n" + "="*50)
    print("🍕 PIZZERÍA - SISTEMA DE GESTIÓN")
    print("="*50)
    print("1. 👤 Clientes")
    print("2. 🍕 Productos")
    print("3. 🛒 Pedidos")
    print("0. 🚪 Salir")

def menu_clientes():
    while True:
        print("\n--- CLIENTES ---")
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("0. Volver")
        op = input("Opción: ")

        if op == '1':
            nombre = input("Nombre: ")
            direccion = input("Dirección: ")
            telefono = input("Teléfono: ")
            ClienteService.crear_cliente(nombre, direccion, int(telefono) if telefono else None)
        elif op == '2':
            clientes = ClienteService.listar_clientes()
            if not clientes:
                print("No hay clientes.")
            else:
                for c in clientes:
                    print(f"ID:{c[0]} | {c[1]} | {c[2]} | {c[3]}")
        elif op == '3':
            cid = int(input("ID del cliente: "))
            nombre = input("Nuevo nombre (Enter = no cambio): ")
            direccion = input("Nueva dirección: ")
            telefono = input("Nuevo teléfono: ")
            ClienteService.actualizar_cliente(
                cid,
                nombre if nombre else None,
                direccion if direccion else None,
                int(telefono) if telefono else None
            )
            print("✅ Actualizado (si existía)")
        elif op == '4':
            cid = int(input("ID del cliente a eliminar: "))
            if ClienteService.eliminar_cliente(cid):
                print("✅ Eliminado")
            else:
                print("❌ No se pudo eliminar (puede tener pedidos asociados)")
        elif op == '0':
            break

def menu_productos():
    while True:
        print("\n--- PRODUCTOS ---")
        print("1. Listar productos")
        print("2. Cambiar precio a un producto")
        print("0. Volver")
        op = input("Opción: ")

        if op == '1':
            prods = ProductoService.listar_productos()
            if not prods:
                print("No hay productos.")
            else:
                print(f"{'ID':<4} {'Pizza':<20} {'Panzerotti':<15} {'Bebida':<15} {'Postre':<15} {'Precio':<8}")
                for p in prods:
                    print(f"{p[0]:<4} {p[1] or '':<20} {p[2] or '':<15} {p[3] or '':<15} {p[4] or '':<15} ${p[5]:<8.2f}")
        elif op == '2':
            pid = int(input("ID del producto: "))
            nuevo_precio = float(input("Nuevo precio: "))
            if ProductoService.actualizar_precio(pid, nuevo_precio):
                print("✅ Precio actualizado")
            else:
                print("❌ Producto no encontrado")
        elif op == '0':
            break

def menu_pedidos():
    while True:
        print("\n--- PEDIDOS ---")
        print("1. Crear nuevo pedido")
        print("2. Listar pedidos")
        print("3. Ver detalle de un pedido")
        print("4. Cambiar estado de un pedido")
        print("0. Volver")
        op = input("Opción: ")

        if op == '1':
            clientes = ClienteService.listar_clientes()
            if not clientes:
                print("❌ No hay clientes. Cree uno primero.")
                continue
            print("Clientes disponibles:")
            for c in clientes:
                print(f"ID: {c[0]} - {c[1]}")
            cliente_id = int(input("ID del cliente: "))

            print("Tipo de pedido: 1=En tienda, 2=Para llevar")
            tipo_op = input("Opción: ")
            tipo = 'tienda' if tipo_op == '1' else 'fuera'
            mesa = None
            if tipo == 'tienda':
                mesa = int(input("Número de mesa: "))

            productos = ProductoService.listar_productos()
            if not productos:
                print("❌ No hay productos registrados.")
                continue
            print("\nProductos disponibles:")
            for p in productos:
                print(f"ID: {p[0]} - {p[1] or p[2] or p[3] or p[4]} - ${p[5]:.2f}")

            items = []
            while True:
                prod_id = input("ID producto (0 para terminar): ")
                if prod_id == '0':
                    break
                prod_id = int(prod_id)
                prod = ProductoService.obtener_producto(prod_id)
                if not prod:
                    print("Producto no existe")
                    continue
                cant = int(input("Cantidad: "))
                items.append({'producto_id': prod_id, 'cantidad': cant})

            if items:
                resultado = PedidoService.crear_pedido(cliente_id, tipo, items, mesa)
                if resultado:
                    print(f"✅ Pedido #{resultado['pedido_id']} registrado. Total: ${resultado['total']:.2f}")
            else:
                print("No se agregaron productos.")

        elif op == '2':
            pedidos = PedidoService.listar_pedidos()
            if not pedidos:
                print("No hay pedidos.")
            else:
                print(f"{'ID':<5} {'Cliente':<20} {'Fecha':<25} {'Total':<10} {'Estado'}")
                for p in pedidos:
                    print(f"{p[0]:<5} {p[1]:<20} {p[2]:<25} ${p[3]:<10.2f} {p[4]}")
        elif op == '3':
            pid = int(input("ID del pedido: "))
            detalle = PedidoService.obtener_pedido_completo(pid)
            if detalle:
                print(f"\nPedido #{detalle['id']}")
                print(f"Cliente: {detalle['cliente']}")
                print(f"Fecha: {detalle['fecha']}")
                print(f"Estado: {detalle['estado']}")
                print("Productos:")
                for d in detalle['detalles']:
                    print(f"  {d['cantidad']} x {d['producto']} - ${d['precio']:.2f} c/u")
                print(f"Total: ${detalle['total']:.2f}")
            else:
                print("Pedido no encontrado.")
        elif op == '4':
            pid = int(input("ID del pedido: "))
            print("Estados posibles: pendiente, pagado, cancelado")
            nuevo_estado = input("Nuevo estado: ")
            if PedidoService.actualizar_estado(pid, nuevo_estado):
                print("✅ Estado actualizado")
            else:
                print("❌ No se pudo actualizar")
        elif op == '0':
            break

def main():
    try:
        conn = db_instance.connect()
        db_instance.disconnect(conn)
        print("✅ Conectado a PostgreSQL")
    except Exception as e:
        print(f"❌ No se pudo conectar: {e}")
        return

    while True:
        menu_principal()
        opcion = input("Seleccione: ")
        if opcion == '1':
            menu_clientes()
        elif opcion == '2':
            menu_productos()
        elif opcion == '3':
            menu_pedidos()
        elif opcion == '0':
            print("👋 Hasta luego")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()