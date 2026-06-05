"""
Servicio para la entidad Productos (bicicletas, repuestos, etc.).
"""

from src.config.database import dbInstance

class ProductoService:
    """Operaciones relacionadas con productos."""

    @staticmethod
    def getAllProducts():
        """Retorna todos los productos con id, tipo, stock, precio y detalles."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_producto, tipo, cantidad_producto, precio_unitario, detalles
                FROM Productos
                ORDER BY id_producto
            """)
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def getProductById(productId):
        """Retorna un solo producto o None."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_producto, tipo, cantidad_producto, precio_unitario, detalles
                FROM Productos
                WHERE id_producto = %s
            """, (productId,))
            return cur.fetchone()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def updateProductPrice(productId, newPrice):
        """Actualiza el precio unitario de un producto."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Productos SET precio_unitario = %s WHERE id_producto = %s",
                        (newPrice, productId))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al actualizar precio: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def updateProductStock(productId, newStock):
        """Actualiza la cantidad disponible en stock."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Productos SET cantidad_producto = %s WHERE id_producto = %s",
                        (newStock, productId))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al actualizar stock: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def addStock(productId, quantity, unitPurchasePrice, supplierId):
        """Transacción para entrada de inventario (compra a proveedor)."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            conn.autocommit = False

            # 1. Bloquear producto y leer stock actual
            cur.execute("SELECT cantidad_producto FROM Productos WHERE id_producto = %s FOR UPDATE", (productId,))
            row = cur.fetchone()
            if not row:
                raise Exception("Producto no encontrado")
            currentStock = row[0]

            # 2. Aumentar stock
            newStock = currentStock + quantity
            cur.execute("UPDATE Productos SET cantidad_producto = %s WHERE id_producto = %s", (newStock, productId))

            # 3. Generar nuevo ID para la orden de compra
            cur.execute("SELECT COALESCE(MAX(id_orden), 0) + 1 FROM Ordenes")
            newOrderId = cur.fetchone()[0]

            totalPrice = unitPurchasePrice * quantity
            cur.execute("""
                INSERT INTO Ordenes (id_orden, fecha, precio, cantidad_compra, id_proveedor, id_producto)
                VALUES (%s, NOW(), %s, %s, %s, %s)
            """, (newOrderId, totalPrice, quantity, supplierId, productId))

            # 4. Registrar movimiento de inventario (entrada)
            cur.execute("""
                INSERT INTO MovimientoInventario (producto_id, tipo, cantidad, referencia)
                VALUES (%s, 'entrada', %s, %s)
            """, (productId, quantity, f"Compra #{newOrderId}"))

            conn.commit()
            print(f"✅ Entrada registrada: +{quantity} unidades de producto {productId}")
            return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Error en entrada de stock: {e}")
            return False
        finally:
            conn.autocommit = True
            cur.close()
        dbInstance.disconnect(conn)

    @staticmethod
    def getMovimientosProducto(productId, limite=50):
        """
        Retorna los últimos movimientos de un producto específico.
        """
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT m.id_movimiento, m.tipo, m.cantidad, m.referencia, m.fecha, m.usuario,
                    p.tipo AS producto_nombre
                FROM MovimientoInventario m
                JOIN Productos p ON m.producto_id = p.id_producto
                WHERE m.producto_id = %s
                ORDER BY m.fecha DESC
                LIMIT %s
            """, (productId, limite))
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)