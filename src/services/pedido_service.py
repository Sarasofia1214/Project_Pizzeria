"""
Servicio para Pedido (órdenes de clientes).
Incluye transacción para insertar pedido y actualizar inventario.
"""

from datetime import datetime
from src.config.database import dbInstance

class PedidoService:
    """Maneja la creación y consulta de pedidos con soporte transaccional."""

    @staticmethod
    def createOrder(customerId, productId, quantity, color=None, size=None, customName=None):
        """
        Crea un nuevo pedido para un cliente.
        Es una transacción: inserta en Pedido y actualiza stock de Productos.
        Retorna el ID del pedido y el total, o None en caso de error.
        """
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            # Iniciar transacción
            conn.autocommit = False

            # 1. Obtener detalles del producto y verificar stock
            cur.execute("""
                SELECT cantidad_producto, precio_unitario
                FROM Productos
                WHERE id_producto = %s
                FOR UPDATE
            """, (productId,))
            row = cur.fetchone()
            if not row:
                raise Exception("Producto no encontrado")
            currentStock, unitPrice = row
            if currentStock < quantity:
                raise Exception(f"Stock insuficiente. Disponible: {currentStock}")

            # 2. Calcular precio total
            totalPrice = unitPrice * quantity

            # 3. Insertar en la tabla Pedido (generar id_pedido manualmente)
            cur.execute("SELECT COALESCE(MAX(id_pedido), 0) + 1 FROM Pedido")
            newOrderId = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO Pedido (id_pedido, nombre, descripcion, precio, color, tamano, id_inventario)
                VALUES (%s, %s, %s, %s, %s, %s, NULL)
            """, (newOrderId, customName or f"Pedido {newOrderId}", f"Pedido del producto {productId}", totalPrice, color, size))

            # 4. Actualizar stock del producto
            newStock = currentStock - quantity
            cur.execute("UPDATE Productos SET cantidad_producto = %s WHERE id_producto = %s",
                        (newStock, productId))

            # 5. Registrar en Tienda (tabla puente)
            cur.execute("""
                INSERT INTO Tienda (id_pedido, id_cliente, destino, id_inventario)
                VALUES (%s, %s, %s, NULL)
            """, (newOrderId, customerId, "En línea"))

            # 6. Registrar en Historial_venta
            cur.execute("SELECT COALESCE(MAX(id_venta), 0) + 1 FROM Historial_venta")
            newSaleId = cur.fetchone()[0]
            cur.execute("INSERT INTO Historial_venta (id_venta, id_pedido) VALUES (%s, %s)",
                        (newSaleId, newOrderId))

            # 7. Confirmar transacción
            conn.commit()
            print(f"✅ Pedido #{newOrderId} creado exitosamente. Total: ${totalPrice:.2f}")
            return {'orderId': newOrderId, 'total': totalPrice}

        except Exception as e:
            conn.rollback()
            print(f"❌ Falló la creación del pedido: {e}")
            return None
        finally:
            conn.autocommit = True
            cur.close()
            dbInstance.disconnect(conn)

        
    @staticmethod
    def getAllOrders():
        """Retorna lista de todos los pedidos con nombre del cliente."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT p.id_pedido, c.nombre AS cliente, p.nombre, p.precio, p.fecha
                FROM Pedido p
                LEFT JOIN Tienda t ON p.id_pedido = t.id_pedido
                LEFT JOIN Cliente c ON t.id_cliente = c.id_cliente
                ORDER BY p.id_pedido DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)
    @staticmethod
    def getOrderDetails(orderId):
        """Retorna detalles completos de un pedido específico."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            # Cabecera del pedido
            cur.execute("""
                SELECT p.id_pedido, p.nombre, p.descripcion, p.precio, p.color, p.tamano, p.fecha,
                       c.nombre AS cliente
                FROM Pedido p
                LEFT JOIN Tienda t ON p.id_pedido = t.id_pedido
                LEFT JOIN Cliente c ON t.id_cliente = c.id_cliente
                WHERE p.id_pedido = %s
            """, (orderId,))
            order = cur.fetchone()
            if not order:
                return None

            return {
                'id': order[0],
                'nombre': order[1],
                'descripcion': order[2],
                'precio': float(order[3]),
                'color': order[4],
                'tamano': order[5],
                'fecha': order[6],
                'cliente': order[7]
            }
        finally:
            cur.close()
            dbInstance.disconnect(conn)